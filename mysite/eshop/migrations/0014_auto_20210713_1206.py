# Generated by Django 3.2.5 on 2021-07-13 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0013_auto_20210713_1158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
