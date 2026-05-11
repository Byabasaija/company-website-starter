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
    newsletter_enabled = models.BooleanField(default=True)

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
    variant      = models.CharField(max_length=50, default='default', blank=True,
                                    help_text='Layout variant. Leave blank for default. '
                                              'services: list, showcase | team: minimal | '
                                              'testimonials: grid | about: centered')
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


class HeroSlide(models.Model):
    RIGHT_PANEL_CHOICES = [
        ('none',     'None'),
        ('services', 'Services'),
        ('events',   'Upcoming Events'),
        ('news',     'Latest News'),
    ]

    headline         = models.CharField(max_length=200, default='Welcome',
                                        help_text='Wrap words in &lt;em&gt; to highlight them in accent colour')
    subheadline      = models.CharField(max_length=300, blank=True)
    cta_text         = models.CharField(max_length=50, default='Learn More')
    cta_url          = models.CharField(max_length=200, default='/')
    cta2_text        = models.CharField(max_length=50, blank=True, verbose_name='Secondary CTA label')
    cta2_url         = models.CharField(max_length=200, blank=True, verbose_name='Secondary CTA URL')
    right_panel      = models.CharField(max_length=20, choices=RIGHT_PANEL_CHOICES, default='events',
                                        verbose_name='Right panel content')
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    order            = models.PositiveIntegerField(default=0)
    is_active        = models.BooleanField(default=True)

    class Meta:
        ordering    = ['order']
        verbose_name = 'Hero Slide'
        verbose_name_plural = 'Hero Slides'

    def __str__(self):
        return self.headline


class HeroImage(models.Model):
    image     = models.ImageField(upload_to='hero/')
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering    = ['order']
        verbose_name = 'Hero Background Image'
        verbose_name_plural = 'Hero Background Images'

    def __str__(self):
        return f'Hero image #{self.order}'


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
    PLACEMENT_CHOICES = [
        ('primary', 'Top Navigation'),
        ('footer',  'Footer'),
        ('both',    'Both'),
    ]

    label       = models.CharField(max_length=50)
    placement   = models.CharField(max_length=10, choices=PLACEMENT_CHOICES, default='primary',
                                   help_text='Where this link appears')
    page        = models.ForeignKey('pages.Page', null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name='nav_links',
                                    help_text='Pick a page to auto-fill the URL — or leave blank and enter a URL below')
    url         = models.CharField(max_length=200, blank=True, default='',
                                   help_text='Custom URL (used when no page is selected)')
    description = models.CharField(max_length=100, blank=True,
                                   help_text='Short subtitle shown in dropdown (child links only)')
    icon        = models.CharField(max_length=50, blank=True,
                                   help_text='Bootstrap icon e.g. bi-gear (child links only)')
    parent      = models.ForeignKey('self', null=True, blank=True,
                                    on_delete=models.CASCADE, related_name='children',
                                    verbose_name='Parent link',
                                    help_text='Set to make this a dropdown item under another link')
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.parent.label} → {self.label}' if self.parent else self.label

    @property
    def get_url(self):
        if self.page_id:
            return self.page.get_absolute_url()
        return self.url or '#'


class FooterLink(models.Model):
    label     = models.CharField(max_length=50)
    url       = models.CharField(max_length=200)
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.label
