# Generated by Django 3.2 on 2023-08-25 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_listing_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='updated_price',
            field=models.FloatField(default=0),
        ),
    ]
