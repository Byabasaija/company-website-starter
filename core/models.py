from django.db import models


class SiteConfig(models.Model):
    site_name       = models.CharField(max_length=100, default='My Company')
    tagline         = models.CharField(max_length=200, blank=True)
    logo            = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon         = models.ImageField(upload_to='site/', blank=True, null=True)
    primary_color   = models.CharField(max_length=7, default='#1a56a0')
    secondary_color = models.CharField(max_length=7, default='#f5a623')
    email           = models.EmailField(blank=True)
    phone           = models.CharField(max_length=20, blank=True)
    address         = models.TextField(blank=True)
    footer_text     = models.CharField(max_length=200, blank=True)
    facebook        = models.URLField(blank=True)
    twitter         = models.URLField(blank=True)
    instagram       = models.URLField(blank=True)
    linkedin        = models.URLField(blank=True)
    youtube         = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Site Configuration'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class HomepageSection(models.Model):
    SECTION_TYPES = [
        ('hero',         'Hero Banner'),
        ('about',        'About Us'),
        ('services',     'Services / Programs'),
        ('team',         'Our Team'),
        ('events',       'Upcoming Events'),
        ('gallery',      'Photo Gallery'),
        ('testimonials', 'Testimonials'),
        ('partners',     'Partners & Sponsors'),
        ('news',         'Latest News / Blog'),
        ('faq',          'FAQ'),
    ]
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES, unique=True)
    order        = models.PositiveIntegerField(default=0)
    is_active    = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.get_section_type_display()} (order: {self.order})'


class HeroSection(models.Model):
    headline     = models.CharField(max_length=200, default='Welcome')
    subheadline  = models.CharField(max_length=300, blank=True)
    cta_text     = models.CharField(max_length=50, default='Learn More')
    cta_url      = models.CharField(max_length=200, default='/about/')
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True)

    class Meta:
        verbose_name = 'Hero Section'

    def __str__(self):
        return self.headline


class AboutSection(models.Model):
    heading = models.CharField(max_length=200, default='About Us')
    body    = models.TextField(blank=True)
    image   = models.ImageField(upload_to='about/', blank=True, null=True)

    class Meta:
        verbose_name = 'About Section'

    def __str__(self):
        return self.heading


class TeamMember(models.Model):
    name      = models.CharField(max_length=100)
    role      = models.CharField(max_length=100)
    photo     = models.ImageField(upload_to='team/', blank=True, null=True)
    bio       = models.TextField(blank=True)
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    facebook  = models.URLField(blank=True)
    twitter   = models.URLField(blank=True)
    linkedin  = models.URLField(blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.name} — {self.role}'


class Service(models.Model):
    title       = models.CharField(max_length=100)
    description = models.TextField()
    icon        = models.CharField(max_length=50, default='bi-star', help_text='Bootstrap icon name e.g. bi-trophy')
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name         = models.CharField(max_length=100)
    role         = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=100, blank=True)
    quote        = models.TextField()
    photo        = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    order        = models.PositiveIntegerField(default=0)
    is_active    = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.name} — {self.organization}'


class Partner(models.Model):
    name        = models.CharField(max_length=100)
    logo        = models.ImageField(upload_to='partners/')
    website_url = models.URLField(blank=True)
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class NavLink(models.Model):
    label     = models.CharField(max_length=50)
    url       = models.CharField(max_length=200)
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label


class FooterLink(models.Model):
    label     = models.CharField(max_length=50)
    url       = models.CharField(max_length=200)
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label
