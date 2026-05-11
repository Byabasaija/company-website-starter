from django.contrib import admin
from .models import Page, PageSection


class PageSectionInline(admin.TabularInline):
    model  = PageSection
    extra  = 1
    fields = ('section_type', 'variant', 'order', 'is_active')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display  = ('title', 'slug', 'is_published', 'created_at')
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    fields  = ('title', 'slug', 'subtitle', 'meta_description', 'is_published')
    inlines = [PageSectionInline]
