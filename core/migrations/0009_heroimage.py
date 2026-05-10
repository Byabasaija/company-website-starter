from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0008_heroslide'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroImage',
            fields=[
                ('id',        models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image',     models.ImageField(upload_to='hero/')),
                ('order',     models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name':        'Hero Background Image',
                'verbose_name_plural': 'Hero Background Images',
                'ordering':            ['order'],
            },
        ),
    ]
