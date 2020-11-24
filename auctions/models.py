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
    bid_amount = models.IntegerField(default=100)
    bid_made_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bid_owner", default="")
    for_which_listing = models.ForeignKey(
        auction_listing, on_delete=models.CASCADE, default="")


class comment(models.Model):
    who_added = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_owner", default="")
    when_added = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=2500, default="A comment")
    for_which_listing = models.ForeignKey(
        auction_listing, on_delete=models.CASCADE, default="")
