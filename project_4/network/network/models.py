from django.contrib.auth.models import AbstractUser
from django.db import models
from asyncio.windows_events import NULL
from unittest.util import _MAX_LENGTH


class User(AbstractUser):
    pass

class Posts(models.Model):
    user_post = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post")
    content_post = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    number_of_likes = models.ManyToManyField(User, blank=True, related_name="user_post")

class Follow(models.Model):
    want_follow = models.ForeignKey("User", on_delete=models.CASCADE, related_name="want_follow")
    is_followed = models.ForeignKey("User", on_delete=models.CASCADE, related_name="is_followed")


