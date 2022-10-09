from django.db import models
from django.contrib.auth.models import User
from django.db.models import ManyToManyField
from auction.models import Auction


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name="userprofile")
    city = models.CharField(max_length=255)
    favorites = models.ManyToManyField(Auction, null=True)
    address = models.CharField(max_length=255)
    signed_up = models.DateTimeField(auto_now_add=True)
    photo = models.TextField(null=True)
    account_type = models.BooleanField(default=False)

    def favorites_set(self):
        self.favorites.clear()

    def __str__(self):
        return self.user
