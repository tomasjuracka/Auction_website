from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
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


@login_required
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        descr = request.POST.get('descr').strip()
        if len(name) > 0:
            category = Category.objects.create(
                creator=request.user,
                name=name,
                description=descr
            )
            return redirect('category', pk=category.id)

    return render(request, 'auction/create_category.html')


def auction(request, pk):
    auction = Auction.objects.get(id=pk)
    profile = Profile.objects.get(id=request.user.id)
    if auction.start_date < timezone.now() < auction.end_date:
        auction.active = True
    else:
        auction.active = False

    context = {'auction': auction, "profile": profile}
    return render(request, "auction/auction.html", context)


def auctions(request):
    auctions = Auction.objects.all()

    context = {'auctions': auctions}
    return render(request, "auction/auctions.html", context)


def create_auction(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        category_name = request.POST.get('category').strip()
        category = Category.objects.get(name=category_name)
        descr = request.POST.get('descr').strip()
        buy_now = request.POST.get('buy_now').strip()
        start_bid = request.POST.get('start_bid').strip()
        start_date = request.POST.get('start_date').strip()
        end_date = request.POST.get('end_date').strip()
        file_url = ""
        if request.FILES.get('upload'):
            upload = request.FILES['upload']
            file_storage = FileSystemStorage()
            file = file_storage.save(upload.name, upload)
            file_url = file_storage.url(file)


        if len(name) > 0 and len(descr) > 0 and len(start_bid) > 0:
            auction = Auction.objects.create(
                seller=request.user,
                name=name,
                description=descr,
                category=category,
                buy_now=buy_now,
                start_bid=start_bid,
                start_date=start_date,
                end_date=end_date,
                active=False
            )
            auction.save()

            return redirect('auction', pk=auction.id)
    categories=Category.objects.all()
    context = {'categories': categories}
    return render(request, 'auction/create_auction.html', context)


def ratings(request):
    ratings = Rating.objects.all()

    context = {'ratings': ratings}
    return render(request, "auction/ratings.html", context)


@login_required
def favorites(request):
    profile = Profile.objects.get(id=request.user.id)
    favorites = profile.favorites.all()

    context = {'auctions': favorites}
    return render(request, "auction/favorites.html", context)


@login_required
def add_favorites(request, id_item):
    auction = Auction.objects.get(id=id_item)
    Profile.objects.get(user=request.user).favorites.add(auction)

    return redirect("auction", pk=id_item)


@login_required
def remove_favorites(request, id_item):
    auction = Auction.objects.get(id=id_item)
    Profile.objects.get(user=request.user).favorites.remove(auction)

    return redirect("auction", pk=id_item)
