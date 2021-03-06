# Generated by Django 2.1.3 on 2018-12-10 15:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('etsy_core', '0028_auto_20181207_1735'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('zipcode', models.IntegerField(validators=[django.core.validators.MaxValueValidator(99999)], verbose_name='zipcode')),
                ('city', models.CharField(max_length=50, verbose_name='city')),
                ('country', models.CharField(max_length=50, verbose_name='country')),
                ('street', models.CharField(max_length=50, verbose_name='street_name')),
            ],
        ),
    ]
