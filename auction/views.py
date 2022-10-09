from django.shortcuts import render
from auction.models import Category, Auction, Rating


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

    context = {'auction': auction}
    return render(request, "auction/auction.html", context)


def auctions(request):
    auctions = Auction.objects.all()

    context = {'auctions': auctions}
    return render(request, "auction/auctions.html", context)


def ratings(request):
    ratings = Rating.objects.all()

    context = {'ratings': ratings}
    return render(request, "auction/ratings.html", context)
