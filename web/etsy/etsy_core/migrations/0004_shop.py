# Generated by Django 2.1.1 on 2018-10-03 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etsy_core', '0003_auto_20180929_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, null=True, verbose_name='shop_name')),
                ('language', models.CharField(max_length=20, null=True, verbose_name='shop_language')),
                ('currency', models.CharField(max_length=45, null=True, verbose_name='shop_currency')),
            ],
        ),
    ]