# Generated by Django 3.2.5 on 2021-07-20 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0024_productreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='rating',
            field=models.IntegerField(choices=[(1, 'Poor'), (2, 'Average'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')], default=1),
        ),
    ]
