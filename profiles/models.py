from django.db import models
from django.utils.text import slugify


class ProfileCategory(models.Model):
    name  = models.CharField(max_length=100)
    slug  = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Profile Categories'

    def __str__(self):
        return self.name


class Profile(models.Model):
    category  = models.ForeignKey(ProfileCategory, on_delete=models.CASCADE, related_name='profiles')
    name      = models.CharField(max_length=100)
    slug      = models.SlugField(unique=True, blank=True)
    role      = models.CharField(max_length=100)
    photo     = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio       = models.TextField(blank=True)
    email     = models.EmailField(blank=True)
    phone     = models.CharField(max_length=20, blank=True)
    facebook  = models.URLField(blank=True)
    twitter   = models.URLField(blank=True)
    linkedin  = models.URLField(blank=True)
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            slug = base
            n = 1
            while Profile.objects.filter(slug=slug).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)
