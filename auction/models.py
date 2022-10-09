from django.db import models

from django.contrib.auth.models import AbstractUser, User


# class User(AbstractUser):
#    pass


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Auction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2047)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    photo = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    ended = models.DateTimeField()
    startBid = models.DecimalField(max_digits=9, decimal_places=2)
    active = models.BooleanField()

    def __str__(self):
        return self.name


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    bid_amount = models.DecimalField(max_digits=9, decimal_places=2)


class Rating(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    # buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment_buyer = models.CharField(max_length=255)
    comment_seller = models.CharField(max_length=255)
    rating_buyer = models.PositiveSmallIntegerField()
    rating_seller = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
