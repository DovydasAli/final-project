# Generated by Django 3.2.5 on 2021-07-05 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0004_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name': 'Sub category', 'verbose_name_plural': 'Sub categories'},
        ),
    ]
