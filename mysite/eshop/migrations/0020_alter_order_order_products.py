# Generated by Django 3.2.5 on 2021-07-14 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0019_auto_20210714_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_products',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='eshop.orderproduct'),
        ),
    ]
