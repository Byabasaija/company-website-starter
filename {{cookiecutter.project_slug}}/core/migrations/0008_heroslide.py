from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0007_nav_profiles_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroSlide',
            fields=[
                ('id',               models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline',         models.CharField(default='Welcome', max_length=200,
                                                      help_text='Wrap words in <em> to highlight them in accent colour')),
                ('subheadline',      models.CharField(blank=True, max_length=300)),
                ('cta_text',         models.CharField(default='Learn More', max_length=50)),
                ('cta_url',          models.CharField(default='/', max_length=200)),
                ('cta2_text',        models.CharField(blank=True, max_length=50, verbose_name='Secondary CTA label')),
                ('cta2_url',         models.CharField(blank=True, max_length=200, verbose_name='Secondary CTA URL')),
                ('background_image', models.ImageField(blank=True, null=True, upload_to='hero/')),
                ('order',            models.PositiveIntegerField(default=0)),
                ('is_active',        models.BooleanField(default=True)),
            ],
            options={
                'verbose_name':        'Hero Slide',
                'verbose_name_plural': 'Hero Slides',
                'ordering':            ['order'],
            },
        ),
    ]
