from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id',               models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title',            models.CharField(max_length=200)),
                ('slug',             models.SlugField(max_length=200, unique=True, blank=True)),
                ('subtitle',         models.CharField(max_length=300, blank=True)),
                ('meta_description', models.CharField(max_length=300, blank=True)),
                ('is_published',     models.BooleanField(default=False)),
                ('created_at',       models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['title']},
        ),
        migrations.CreateModel(
            name='PageSection',
            fields=[
                ('id',           models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_type', models.CharField(max_length=50, choices=[
                    ('about',        'About Us'),
                    ('services',     'Services / Programs'),
                    ('team',         'Our Team'),
                    ('events',       'Upcoming Events'),
                    ('gallery',      'Photo Gallery'),
                    ('testimonials', 'Testimonials'),
                    ('partners',     'Partners & Sponsors'),
                    ('news',         'Latest News / Blog'),
                    ('faq',          'FAQ'),
                    ('newsletter',   'Newsletter Signup'),
                ])),
                ('order',        models.PositiveIntegerField(default=0)),
                ('is_active',    models.BooleanField(default=True)),
                ('page',         models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='pages.page')),
            ],
            options={'ordering': ['order'], 'unique_together': {('page', 'section_type')}},
        ),
    ]
