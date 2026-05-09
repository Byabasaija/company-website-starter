from django.contrib import admin
from core.widgets import TrixWidget
from django import forms
from .models import ProfileCategory, Profile


class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {'bio': TrixWidget()}


class ProfileInline(admin.StackedInline):
    model = Profile
    form  = ProfileAdminForm
    extra = 0
    fields = ('name', 'role', 'photo', 'bio', 'email', 'phone',
              'facebook', 'twitter', 'linkedin', 'order', 'is_active')


@admin.register(ProfileCategory)
class ProfileCategoryAdmin(admin.ModelAdmin):
    list_display  = ('name', 'slug', 'order')
    list_editable = ('order',)
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProfileInline]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form              = ProfileAdminForm
    list_display      = ('name', 'role', 'category', 'order', 'is_active')
    list_editable     = ('order', 'is_active')
    list_filter       = ('category', 'is_active')
    search_fields     = ('name', 'role')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Identity', {'fields': ('category', 'name', 'slug', 'role', 'photo')}),
        ('Bio',      {'fields': ('bio',)}),
        ('Contact',  {'fields': ('email', 'phone')}),
        ('Social',   {'fields': ('facebook', 'twitter', 'linkedin')}),
        ('Settings', {'fields': ('order', 'is_active')}),
    )
