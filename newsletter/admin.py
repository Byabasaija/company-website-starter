from django.contrib import admin
from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display  = ('email', 'confirmed', 'created_at')
    list_filter   = ('confirmed',)
    readonly_fields = ('token', 'created_at')
