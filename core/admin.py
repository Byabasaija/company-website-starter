from django.contrib import admin
from .models import (SiteConfig, HomepageSection, HeroSection, AboutSection,
                     TeamMember, Service, Testimonial, Partner, NavLink, FooterLink)


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identity', {'fields': ('site_name', 'tagline', 'logo', 'favicon')}),
        ('Brand Colors', {'fields': ('primary_color', 'secondary_color')}),
        ('Contact', {'fields': ('email', 'phone', 'address')}),
        ('Social Links', {'fields': ('facebook', 'twitter', 'instagram', 'linkedin', 'youtube')}),
        ('Footer', {'fields': ('footer_text',)}),
    )

    def has_add_permission(self, request):
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HomepageSection)
class HomepageSectionAdmin(admin.ModelAdmin):
    list_display  = ('get_section_type_display', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering      = ('order',)


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    pass


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    pass


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display  = ('name', 'role', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
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


@admin.register(NavLink)
class NavLinkAdmin(admin.ModelAdmin):
    list_display  = ('label', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display  = ('label', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active')
