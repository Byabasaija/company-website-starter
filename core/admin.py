from django import forms
from django.contrib import admin
from .models import (SiteConfig, HomepageSection, HeroSection, HeroSlide, HeroImage, AboutSection,
                     TeamMember, Service, Testimonial, Partner, NavLink)
from .widgets import TrixWidget


class AboutSectionAdminForm(forms.ModelForm):
    class Meta:
        model = AboutSection
        fields = '__all__'
        widgets = {'body': TrixWidget()}


class ServiceAdminForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        widgets = {'description': TrixWidget()}


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identity', {'fields': ('site_name', 'tagline', 'logo', 'favicon')}),
        ('Brand Colors', {'fields': ('primary_color', 'secondary_color')}),
        ('Contact', {'fields': ('email', 'phone', 'address')}),
        ('Social Links', {'fields': ('facebook', 'twitter', 'instagram', 'linkedin', 'youtube')}),
        ('Footer', {'fields': ('footer_text',)}),
        ('Features', {'fields': ('newsletter_enabled',)}),
    )

    def has_add_permission(self, request):
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HomepageSection)
class HomepageSectionAdmin(admin.ModelAdmin):
    list_display  = ('get_section_type_display', 'variant', 'order', 'is_active')
    list_editable = ('variant', 'order', 'is_active')
    ordering      = ('order',)


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    pass


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display  = ('headline', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    fieldsets = (
        ('Content', {'fields': ('headline', 'subheadline')}),
        ('Primary CTA', {'fields': ('cta_text', 'cta_url')}),
        ('Secondary CTA', {'fields': ('cta2_text', 'cta2_url'), 'classes': ('collapse',)}),
        ('Layout', {'fields': ('right_panel',)}),
        ('Settings', {'fields': ('order', 'is_active')}),
    )


@admin.register(HeroImage)
class HeroImageAdmin(admin.ModelAdmin):
    list_display  = ('__str__', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    form = AboutSectionAdminForm


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display  = ('name', 'role', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    form          = ServiceAdminForm
    list_display  = ('title', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display  = ('name', 'organization', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display  = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')


class NavChildInline(admin.TabularInline):
    model   = NavLink
    fk_name = 'parent'
    extra   = 1
    fields  = ('label', 'page', 'url', 'icon', 'description', 'order', 'is_active')


@admin.register(NavLink)
class NavLinkAdmin(admin.ModelAdmin):
    list_display  = ('label', 'placement', 'get_url', 'parent', 'order', 'is_active')
    list_editable = ('placement', 'order', 'is_active')
    list_filter   = ('placement', 'parent')
    fieldsets = (
        ('Link', {
            'fields': ('label', 'placement', 'page', 'url'),
        }),
        ('Dropdown', {
            'fields': ('parent', 'icon', 'description'),
            'classes': ('collapse',),
        }),
        ('Settings', {
            'fields': ('order', 'is_active'),
        }),
    )
    inlines = [NavChildInline]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(parent=None)
