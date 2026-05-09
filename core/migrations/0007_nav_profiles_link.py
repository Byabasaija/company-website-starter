from django.db import migrations


def add_profiles_nav(apps, schema_editor):
    NavLink = apps.get_model('core', 'NavLink')
    if not NavLink.objects.filter(url='/profiles/').exists():
        NavLink.objects.filter(label='Blog').update(order=5)
        NavLink.objects.filter(label='Contact').update(order=6)
        NavLink.objects.create(label='People', url='/profiles/', order=4, is_active=True)


def remove_profiles_nav(apps, schema_editor):
    NavLink = apps.get_model('core', 'NavLink')
    NavLink.objects.filter(url='/profiles/').delete()
    NavLink.objects.filter(label='Blog').update(order=4)
    NavLink.objects.filter(label='Contact').update(order=5)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0006_newsletter_enabled'),
    ]
    operations = [
        migrations.RunPython(add_profiles_nav, remove_profiles_nav),
    ]
