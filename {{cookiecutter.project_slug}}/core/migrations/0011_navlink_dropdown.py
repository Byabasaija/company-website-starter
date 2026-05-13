from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0010_heroslide_right_panel'),
    ]

    operations = [
        migrations.AddField(
            model_name='navlink',
            name='description',
            field=models.CharField(
                blank=True, max_length=100,
                help_text='Short subtitle shown in dropdown (child links only)',
            ),
        ),
        migrations.AddField(
            model_name='navlink',
            name='icon',
            field=models.CharField(
                blank=True, max_length=50,
                help_text='Bootstrap icon e.g. bi-gear (child links only)',
            ),
        ),
        migrations.AddField(
            model_name='navlink',
            name='parent',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='children',
                to='core.navlink',
                verbose_name='Parent link',
                help_text='Set to make this a dropdown item under another link',
            ),
        ),
        migrations.AlterField(
            model_name='navlink',
            name='url',
            field=models.CharField(blank=True, default='#', max_length=200),
        ),
    ]
