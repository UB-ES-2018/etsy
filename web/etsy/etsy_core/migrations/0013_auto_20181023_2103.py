# Generated by Django 2.1.1 on 2018-10-23 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etsy_core', '0012_auto_20181022_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='tags_name',
            field=models.CharField(max_length=255, verbose_name='tag_name'),
        ),
    ]
