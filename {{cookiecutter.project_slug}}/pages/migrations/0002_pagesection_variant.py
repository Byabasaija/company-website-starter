from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pagesection',
            name='variant',
            field=models.CharField(
                blank=True, default='default', max_length=50,
                help_text='Layout variant. Leave blank for default. '
                          'services: list, showcase | team: minimal | '
                          'testimonials: grid | about: centered',
            ),
        ),
    ]
