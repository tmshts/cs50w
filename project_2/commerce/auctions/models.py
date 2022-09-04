from asyncio.windows_events import NULL
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name_of_category = models.CharField(max_length=200)

class Listing(models.Model):
    # Provided by user
    title_of_listing = models.CharField(max_length=200)
    description_of_listing = models.TextField()
    image_of_listing = models.URLField(max_length=2000, blank=True)
    starting_bid_of_listing = models.FloatField()
    # blank=False - every listing must have category
    category_of_listing = models.ForeignKey(Category, blank=True, on_delete=models.SET_NULL, null=True, related_name="what_category")
    listed_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_by")
    # when the object is created
    time_of_creation = models.DateTimeField(auto_now_add=True)
    not_active = models.BooleanField(default=False)

class Comment(models.Model):
    content_of_comment = models.TextField()
    comment_in_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comment")
    comment_from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")

class Bid(models.Model):
    price_of_bid = models.FloatField()
    bid_for_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bid")
    bid_from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")

class Watchlist(models.Model):
    watchlist_for_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_watchlist")
    watchlist_from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
