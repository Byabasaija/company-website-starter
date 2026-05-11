from django.db import migrations


def copy_footer_links_to_navlinks(apps, schema_editor):
    FooterLink = apps.get_model('core', 'FooterLink')
    NavLink    = apps.get_model('core', 'NavLink')
    for fl in FooterLink.objects.all():
        NavLink.objects.create(
            label=fl.label,
            url=fl.url,
            placement='footer',
            order=fl.order,
            is_active=fl.is_active,
        )


def reverse_copy(apps, schema_editor):
    NavLink = apps.get_model('core', 'NavLink')
    NavLink.objects.filter(placement='footer').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0013_navlink_placement_page'),
    ]

    operations = [
        migrations.RunPython(copy_footer_links_to_navlinks, reverse_copy),
    ]
