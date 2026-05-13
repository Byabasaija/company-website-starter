# Chess Feature Design Spec

**Target project:** Chess club site generated from `company-website-starter`  
**Status:** Proposed

---

## Overview

Add a `chess` Django app that lets a chess club publish, replay, and annotate games in PGN format. The feature sits entirely within the `chess` app so it can be added to any project generated from the starter template without touching core code.

---

## User stories

| Who | Wants to | So that |
|-----|----------|---------|
| Admin | Upload/paste a PGN and publish a game | Club members can replay it on the site |
| Visitor | Navigate moves forward/backward on an interactive board | They can study the game |
| Visitor | See who played, what event, and the result at a glance | Context is clear without reading the PGN |
| Admin | Attach a game to a tournament event | Games are discoverable from the Events page |
| Visitor | Browse the game archive filtered by player or tournament | They can find games easily |

---

## Data model

### `Game`

| Field | Type | Notes |
|-------|------|-------|
| `title` | `CharField(200)` | Optional display title |
| `slug` | `SlugField(unique=True)` | Auto-generated from title or white vs black |
| `pgn` | `TextField` | Full PGN string, one or more games |
| `white` | `CharField(100)` | White player name |
| `black` | `CharField(100)` | Black player name |
| `result` | `CharField(10)` | `1-0`, `0-1`, `1/2-1/2`, `*` |
| `event` | `ForeignKey('events.Event', null=True, blank=True)` | Links game to a tournament event |
| `round` | `CharField(10, blank=True)` | Round number/label |
| `date_played` | `DateField(null=True, blank=True)` | |
| `annotator` | `CharField(100, blank=True)` | Person who annotated |
| `notes` | `TextField(blank=True)` | Rich text editorial notes shown beside board |
| `is_featured` | `BooleanField(default=False)` | Surfaced on homepage / events page |
| `is_published` | `BooleanField(default=False)` | |
| `created_at` | `DateTimeField(auto_now_add=True)` | |

Auto-generate slug from `f"{white}-vs-{black}"` with uniqueness suffix.

---

## URL structure

```
/games/                          → game list (paginated, filterable)
/games/<slug>/                   → game detail with interactive board
```

---

## Frontend: board rendering

Use **[lichess-pgn-viewer](https://github.com/lichess-org/pgn-viewer)** — open source, zero-dependency library that renders a full interactive board with move list, arrows, and annotations from a PGN string.

### Integration pattern

```html
<!-- In game detail template -->
<div id="pgn-viewer"></div>

<script type="module">
  import { LichessPgnViewer } from 'https://cdn.jsdelivr.net/npm/@lichess-org/pgn-viewer/dist/lichess-pgn-viewer.esm.min.js';
  LichessPgnViewer(document.getElementById('pgn-viewer'), {
    pgn: `{{ game.pgn|escapejs }}`,
    showMoves: 'auto',
    scrollToMove: true,
    orientation: 'white',
  });
</script>
```

CSS (link in `base.html` or scoped to the game detail template):
```html
<link rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@lichess-org/pgn-viewer/dist/lichess-pgn-viewer.css">
```

---

## Pages

### `/games/` — Game list

- Cards: White vs Black, result badge, event name (linked), date
- Filter bar (Alpine.js): by result (`1-0`, `0-1`, `½-½`) and by event
- Pagination: 20 per page

### `/games/<slug>/` — Game detail

- Left: interactive board (lichess-pgn-viewer, full height)
- Right: move list (rendered by the library), metadata, annotator notes

---

## Homepage integration

Optional `HomepageSection` of type `featured-game`:

```html
{# components/sections/featured-game/default.html #}
{% if featured_game %}
<section class="section-padding bg-surface">
  <div class="max-w-7xl mx-auto">
    <span class="section-label">Game of the Week</span>
    <h2 class="section-title">{{ featured_game.white }} vs {{ featured_game.black }}</h2>
    <!-- board rendered here -->
  </div>
</section>
{% endif %}
```

---

## Admin

```python
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display  = ('title_or_matchup', 'result', 'event', 'date_played', 'is_featured', 'is_published')
    list_filter   = ('is_published', 'is_featured', 'result')
    search_fields = ('white', 'black', 'title', 'pgn')
    prepopulated_fields = {'slug': ('white', 'black')}
    fieldsets = (
        (None,         {'fields': ('title', 'slug', 'pgn', 'is_published', 'is_featured')}),
        ('Players',    {'fields': ('white', 'black', 'result', 'round', 'date_played')}),
        ('Context',    {'fields': ('event', 'annotator', 'notes')}),
    )
```

---

## Sitemap

`chess/sitemaps.py` — `GameSitemap` registered in `project/urls.py`.

---

## Files to create

```
chess/__init__.py
chess/apps.py
chess/models.py
chess/admin.py
chess/views.py
chess/urls.py
chess/sitemaps.py
chess/migrations/0001_initial.py
templates/html/chess/list.html
templates/html/chess/detail.html
templates/html/components/sections/featured-game/default.html
tests/test_chess.py
```

## Files to modify

```
project/settings/base.py     (add chess to INSTALLED_APPS)
project/urls.py              (add path('games/', ...), GameSitemap)
project/sitemaps.py          (add games-list to StaticSitemap)
core/views.py                (add featured_game to home_view context)
```
