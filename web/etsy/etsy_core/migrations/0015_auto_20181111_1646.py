# Generated by Django 2.1.3 on 2018-11-11 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('etsy_core', '0014_productimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=255, verbose_name='category_name')),
                ('is_default', models.BooleanField(db_index=True, default=False)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='etsy_core.Categories'),
            preserve_default=False,
        ),
    ]