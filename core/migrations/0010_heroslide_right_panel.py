from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0009_heroimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='heroslide',
            name='right_panel',
            field=models.CharField(
                choices=[
                    ('none',     'None'),
                    ('services', 'Services'),
                    ('events',   'Upcoming Events'),
                    ('news',     'Latest News'),
                ],
                default='events',
                max_length=20,
                verbose_name='Right panel content',
            ),
        ),
    ]
