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
    form          = EventAdminForm
    list_display  = ('title', 'start_date', 'location', 'is_published')
    list_editable = ('is_published',)
    list_filter   = ('is_published',)
    ordering      = ('start_date',)
    prepopulated_fields = {'slug': ('title',)}
