from django.db import migrations


def add_events_nav(apps, schema_editor):
    NavLink = apps.get_model('core', 'NavLink')
    if not NavLink.objects.filter(url='/events/').exists():
        NavLink.objects.filter(label='Blog').update(order=4)
        NavLink.objects.filter(label='Contact').update(order=5)
        NavLink.objects.create(label='Events', url='/events/', order=3, is_active=True)


def remove_events_nav(apps, schema_editor):
    NavLink = apps.get_model('core', 'NavLink')
    NavLink.objects.filter(url='/events/').delete()
    NavLink.objects.filter(label='Blog').update(order=3)
    NavLink.objects.filter(label='Contact').update(order=4)


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_default_data'),
    ]
    operations = [
        migrations.RunPython(add_events_nav, remove_events_nav),
    ]
