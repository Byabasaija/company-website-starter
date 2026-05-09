from django.db import models


class GalleryCategory(models.Model):
    name  = models.CharField(max_length=100)
    slug  = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Gallery categories'

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    category  = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE,
                                  related_name='images')
    image     = models.ImageField(upload_to='gallery/')
    caption   = models.CharField(max_length=200, blank=True)
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.caption or str(self.image)
