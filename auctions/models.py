from django.contrib.auth.models import AbstractUser
from django.db import models


class auction_listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    image_url = models.CharField(max_length=2100)
    active = models.BooleanField(default=True)
    added_when = models.DateTimeField(auto_now_add=True)
    category = models.CharField(default="Other", max_length=32)
    created_by = models.CharField(default="User", max_length=64)

    def __str__(self):
        return f"{self.id}: Product - {self.title}"


class User(AbstractUser):
    watchlist = models.ManyToManyField(auction_listing, related_name='owner')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class bid(models.Model):
    pass


class comment(models.Model):
    pass
