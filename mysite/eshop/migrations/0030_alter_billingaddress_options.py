# Generated by Django 3.2.5 on 2021-07-26 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0029_order_billing_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='billingaddress',
            options={'verbose_name': 'Billing address', 'verbose_name_plural': 'Billing addresses'},
        ),
    ]
