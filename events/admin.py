from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display  = ('title', 'start_date', 'location', 'is_published')
    list_editable = ('is_published',)
    list_filter   = ('is_published',)
    ordering      = ('start_date',)
    prepopulated_fields = {'slug': ('title',)}
