from django.db import models
from django.utils.text import slugify


SECTION_TYPES = [
    ('about',        'About Us'),
    ('services',     'Services / Programs'),
    ('team',         'Our Team'),
    ('events',       'Upcoming Events'),
    ('gallery',      'Photo Gallery'),
    ('testimonials', 'Testimonials'),
    ('partners',     'Partners & Sponsors'),
    ('news',         'Latest News / Blog'),
    ('faq',          'FAQ'),
    ('newsletter',   'Newsletter Signup'),
]


class Page(models.Model):
    title            = models.CharField(max_length=200)
    slug             = models.SlugField(max_length=200, unique=True, blank=True)
    subtitle         = models.CharField(max_length=300, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    is_published     = models.BooleanField(default=False)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('page_detail', kwargs={'slug': self.slug})


class PageSection(models.Model):
    page         = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='sections')
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES)
    variant      = models.CharField(max_length=50, default='default', blank=True,
                                    help_text='Layout variant. Leave blank for default. '
                                              'services: list, showcase | team: minimal | '
                                              'testimonials: grid | about: centered')
    order        = models.PositiveIntegerField(default=0)
    is_active    = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        unique_together = ('page', 'section_type')

    def __str__(self):
        return f'{self.page.title} — {self.get_section_type_display()}'
