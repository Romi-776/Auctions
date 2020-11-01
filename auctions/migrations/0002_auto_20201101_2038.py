# Generated by Django 3.0.8 on 2020-11-01 15:08

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='description',
            field=models.CharField(default='A comment', max_length=2500),
        ),
        migrations.AddField(
            model_name='comment',
            name='for_which_listing',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='auctions.auction_listing'),
        ),
        migrations.AddField(
            model_name='comment',
            name='when_added',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 11, 1, 20, 38, 43, 258373)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='who_added',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='comment_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]