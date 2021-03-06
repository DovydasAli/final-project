# Generated by Django 3.2.5 on 2021-07-07 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0007_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('order placed', 'Order placed'), ('in progress', 'In progress'), ('done', 'Done'), ('canceled', 'Canceled')], default='order placed', help_text='Status', max_length=12),
        ),
    ]
