# Generated by Django 2.1.1 on 2018-10-17 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etsy_core', '0008_auto_20181014_1736'),
    ]

    operations = [
        migrations.AddField(
            model_name='options',
            name='is_default',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]