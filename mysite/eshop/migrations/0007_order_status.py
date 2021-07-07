# Generated by Django 3.2.5 on 2021-07-07 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0006_alter_product_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('order placed', 'Order placed'), ('in progress', 'In progress'), ('done', 'Done'), ('canceled', 'Canceled')], default='draft', help_text='Status', max_length=12),
        ),
    ]