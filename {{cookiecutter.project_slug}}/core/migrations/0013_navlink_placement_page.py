from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0012_homepagesection_variant'),
        ('pages', '0002_pagesection_variant'),
    ]

    operations = [
        migrations.AddField(
            model_name='navlink',
            name='placement',
            field=models.CharField(
                max_length=10,
                choices=[('primary', 'Top Navigation'), ('footer', 'Footer'), ('both', 'Both')],
                default='primary',
                help_text='Where this link appears',
            ),
        ),
        migrations.AddField(
            model_name='navlink',
            name='page',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='nav_links',
                to='pages.page',
                help_text='Pick a page to auto-fill the URL — or leave blank and enter a URL below',
            ),
        ),
        migrations.AlterField(
            model_name='navlink',
            name='url',
            field=models.CharField(
                blank=True, default='', max_length=200,
                help_text='Custom URL (used when no page is selected)',
            ),
        ),
    ]
