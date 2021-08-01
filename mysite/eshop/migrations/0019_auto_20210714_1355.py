# Generated by Django 3.2.5 on 2021-07-14 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0018_auto_20210714_1226'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='order_products',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='eshop.orderproduct'),
            preserve_default=False,
        ),
    ]
