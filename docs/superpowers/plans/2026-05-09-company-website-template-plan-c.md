# Plan C — Company Website Template: Enhancements

**Status:** Backlog — not started  
**Created:** 2026-05-09  
**Depends on:** Plan A ✓, Plan B ✓

---

## Scope

Optional enhancements to the company website template. Each item is independent and can be picked up in any order.

---

## Item 1: Trix Rich-Text Editor in Admin

Replace plain `<textarea>` fields with Trix (ships with Rails but works standalone) so editors can format event descriptions, about body, and service descriptions without writing HTML.

**Affected models:** `Event.description`, `AboutSection.body`, `Service.description`  
**Approach:** Store as HTML in a `TextField`; render with `{{ value|safe }}` in templates (already used for blog body).

---

## Item 2: Newsletter Subscribe Form

Capture email subscribers with a lightweight subscribe form in the footer or as a homepage section.

**Options:**
- Local model (`Subscriber`) with double opt-in via email token
- Mailchimp API integration

**Deliverables:** `newsletter` app, subscribe view, confirmation email, admin list with CSV export, footer partial.

---

## Item 3: SEO Enhancements

- **Per-page OG images** — `og:image` meta tag populated from each page's primary image (hero, event thumbnail, blog thumbnail)
- **Canonical URLs** — `<link rel="canonical">` on all pages
- **JSON-LD structured data** — `Event` schema for event detail pages, `Article` schema for blog posts, `Organization` schema on homepage

---

## Item 4: Gallery Lightbox

Full-screen image viewer when a gallery image is clicked.

**Approach:** Alpine.js + a small CSS overlay — no extra JS library needed.  
**Features:** Open on click, keyboard nav (← →), close on Escape or backdrop click, caption display.

---

## Item 5: Contact Form reCAPTCHA

Add Google reCAPTCHA v3 (invisible) to the inquiry form to block spam submissions.

**Deliverables:** `RECAPTCHA_SITE_KEY` / `RECAPTCHA_SECRET_KEY` settings, server-side score check in `InquiryCreateView`, silent failure mode for development (key not set → skip check).

---

## Item 6: Uganda Chess Federation Features

Specialist features for the UCF use-case.

- **Player profiles** — `Player` model (name, FIDE ID, national rating, photo, bio), list + detail views
- **Tournament brackets** — `Tournament` + `Round` + `Pairing` models; bracket display template
- **Ratings table** — sortable table of top-N players by rating, filterable by category (Open, Women, Junior)

---

## Self-Review Checklist (fill in when executing)

- [ ] Each item has failing tests before implementation
- [ ] No placeholder code left in templates
- [ ] Tailwind recompiled after template changes
- [ ] All existing 31 tests still pass after each item
- [ ] Final commit per item: `feat: <item name>`
