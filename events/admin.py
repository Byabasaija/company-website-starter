from django import forms
from django.contrib import admin
from core.widgets import TrixWidget
from .models import Event


class EventAdminForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        widgets = {'description': TrixWidget()}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    form            = EventAdminForm
    list_display    = ('title', 'start_date', 'end_date', 'location', 'organizer', 'is_published', 'is_past')
    list_editable   = ('is_published',)
    list_filter     = ('is_published',)
    ordering        = ('start_date',)
    readonly_fields = ('is_past',)
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Event', {
            'fields': ('title', 'slug', 'description', 'thumbnail'),
        }),
        ('Schedule & Location', {
            'fields': ('start_date', 'end_date', 'location', 'is_past'),
        }),
        ('Details', {
            'fields': ('organizer', 'sponsor', 'event_link'),
        }),
        ('Publishing', {
            'fields': ('is_published',),
        }),
    )
