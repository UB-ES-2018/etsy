# Generated by Django 2.1.1 on 2018-10-17 14:11

from django.db import migrations, models
import etsy_core.models.user


class Migration(migrations.Migration):

    dependencies = [
        ('etsy_core', '0008_auto_20181014_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=etsy_core.models.user.get_image_path),
        ),
    ]
