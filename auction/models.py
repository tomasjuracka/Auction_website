from django.db import models

from django.contrib.auth.models import AbstractUser, User


# class User(AbstractUser):
#    pass


class Category(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Auction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=2047)
    photo = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    buy_now = models.DecimalField(max_digits=9, decimal_places=2)
    start_bid = models.DecimalField(max_digits=9, decimal_places=2)
    min_bid = models.DecimalField(max_digits=9, decimal_places=2)
    active = models.BooleanField()

    def __str__(self):
        return self.name


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    bid_amount = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)


class Rating(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
