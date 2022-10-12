from django.shortcuts import render, redirect
from auction.models import Category, Auction, Rating

from profiles.models import Profile


# Create your views here.


def home(request):

    return render(request, 'auction/home.html')


def category(request, pk):
    category = Category.objects.get(id=pk)
    auctions = Auction.objects.filter(category=pk)

    context = {'category': category, 'auctions': auctions}
    return render(request, "auction/category.html", context)


def categories(request):
    categories = Category.objects.all()

    context = {'categories': categories}
    return render(request, "auction/categories.html", context)


def auction(request, pk):
    auction = Auction.objects.get(id=pk)
    profile = Profile.objects.get(id=request.user.id)

    context = {'auction': auction, "profile": profile}
    return render(request, "auction/auction.html", context)


def auctions(request):
    auctions = Auction.objects.all()

    context = {'auctions': auctions}
    return render(request, "auction/auctions.html", context)


def ratings(request):
    ratings = Rating.objects.all()

    context = {'ratings': ratings}
    return render(request, "auction/ratings.html", context)


def favorites(request):
    profile = Profile.objects.get(id=request.user.id)
    favorites = profile.favorites.all()

    context = {'auctions': favorites}
    return render(request, "auction/favorites.html", context)


def add_favorites(request, id_item):
    auction = Auction.objects.get(id=id_item)
    Profile.objects.get(user=request.user).favorites.add(auction)

    return redirect("auction", pk=id_item)


def remove_favorites(request, id_item):
    auction = Auction.objects.get(id=id_item)
    Profile.objects.get(user=request.user).favorites.remove(auction)

    return redirect("auction", pk=id_item)
