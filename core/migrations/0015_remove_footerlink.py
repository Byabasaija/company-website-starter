from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0014_copy_footer_links'),
    ]

    operations = [
        migrations.DeleteModel(name='FooterLink'),
    ]
