from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Event(models.Model):
    title        = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True, blank=True)
    description  = models.TextField(blank=True)
    start_date   = models.DateTimeField()
    end_date     = models.DateTimeField(blank=True, null=True)
    location     = models.CharField(max_length=200, blank=True)
    event_link   = models.URLField(blank=True, help_text='Registration or external event page URL')
    organizer    = models.CharField(max_length=200, blank=True)
    sponsor      = models.CharField(max_length=200, blank=True)
    thumbnail    = models.ImageField(upload_to='events/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)

    @property
    def is_past(self):
        cutoff = self.end_date or self.start_date
        if cutoff is None:
            return False
        return cutoff < timezone.now()

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Event.objects.filter(slug=slug).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)
