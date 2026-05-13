from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0015_remove_footerlink'),
    ]

    operations = [
        migrations.DeleteModel(name='HeroSection'),
    ]
