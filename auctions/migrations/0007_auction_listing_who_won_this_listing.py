# Generated by Django 3.0.8 on 2020-11-26 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auction_listing_starting_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction_listing',
            name='who_won_this_listing',
            field=models.CharField(default='', max_length=64),
        ),
    ]
