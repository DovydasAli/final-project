# Generated by Django 3.2.5 on 2021-07-13 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0012_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
