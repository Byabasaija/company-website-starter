from django.contrib import admin
from .models import GalleryCategory, GalleryImage


class GalleryImageInline(admin.TabularInline):
    model  = GalleryImage
    extra  = 3
    fields = ('image', 'caption', 'order', 'is_active')


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display       = ('name', 'slug', 'order')
    list_editable      = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    inlines            = [GalleryImageInline]


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display  = ('__str__', 'category', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter   = ('category', 'is_active')
