from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_link',
            field=models.URLField(blank=True, help_text='Registration or external event page URL'),
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='event',
            name='sponsor',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
