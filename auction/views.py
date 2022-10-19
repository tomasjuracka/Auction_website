from datetime import datetime, date
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Max
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from auction.models import Category, Auction, Rating, Bid
import pytz
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
    profile = Profile.objects.get(user=request.user)
    bids = Bid.objects.filter(auction=auction)
    amount = 0
    bid = None
    active = True
    ended = False
    utc = pytz.UTC
    if utc.localize(datetime.today()) < auction.start_date:
        active = False
    if utc.localize(datetime.today()) > auction.end_date:
        ended = True
    try:
        if bids:
            amount = bids.aggregate(Max('bid_amount'))['bid_amount__max']
            bid = Bid.objects.get(auction=auction, bid_amount=amount)
    except ValueError:
        amount = 0
    if auction.start_date < timezone.now() < auction.end_date:
        auction.active = True
        auction.save()
    else:
        auction.active = False
        auction.save()
    try:
        if auction.buy_now <= amount:
            auction.active = False
            auction.save()
    except TypeError:
        pass
    context = {'auction': auction, "profile": profile, "bids": bids, "max_bid": bid, "active": active, "ended": ended}
    return render(request, "auction/auction.html", context)


def auctions(request):
    auctions = Auction.objects.all()

    message = ''
    request.session["message"] = message

    filter = "all"
    if request.method == "POST":
        explore = request.POST.get("explore")
        if explore == "own":
            auctions = Auction.objects.filter(seller=request.user)
            filter = "My auctions"

        elif explore == "did_bid":
            bids = Bid.objects.filter(user=request.user).distinct()
            auctions = []
            for bid in bids:
                if bid.auction not in auctions:
                    auctions.append(bid.auction)
            filter = "Auctions I bid"

        elif explore == "recent":
            auctions = Auction.objects.order_by("created")[:10]
            filter = "Recently added"

        elif explore == "ending":
            auctions = Auction.objects.order_by("end_date")[:10]
            filter = "Soon ending"

        elif explore == "favorite":
            profile = Profile.objects.get(id=request.user.id)
            auctions = profile.favorites.all()
            filter = "Favorite auctions"

        elif explore == "ended":
            auctions = Auction.objects.filter(end_date__lt=datetime.today())
            filter = "Just ended"

    context = {'auctions': auctions, "filter": filter}
    return render(request, "auction/auctions.html", context)


@login_required
def create_auction(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        category_name = request.POST.get('category').strip()
        category = Category.objects.get(name=category_name)
        descr = request.POST.get('descr').strip()
        buy_now = request.POST.get('buy_now').strip()
        start_bid = request.POST.get('start_bid').strip()
        min_bid = request.POST.get('min_bid').strip()
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
                min_bid=min_bid,
                start_date=start_date,
                end_date=end_date,
                active=False,
                photo=file_url
            )
            auction.save()

            return redirect('auction', pk=auction.id)
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'auction/create_auction.html', context)


def ratings(request):
    ratings = Rating.objects.all()

    context = {'ratings': ratings}
    return render(request, "auction/ratings.html", context)


@login_required
def rating(request, pk):
    if request.method == 'POST':
        auction = Auction.objects.get(id=pk)
        stars = request.POST["stars"]
        comment = request.POST["comment"].strip()
        if comment != "":
            rating = Rating.objects.create(
                auction=auction,
                user=request.user,
                stars=stars,
                comment=comment,
            )
            rating.save()
        return HttpResponseRedirect(reverse("auction", kwargs={'id': pk}))
    return HttpResponseRedirect(reverse("home"))


@login_required
def bid(request, pk):
    message = ''
    request.session["message"] = message
    if request.method == 'POST':
        auction = Auction.objects.get(id=pk)
        bid_amount = request.POST["bid"]
        try:
            bid_amount = float(bid_amount)
        except ValueError:
            bid_amount = 0

        args = Bid.objects.filter(auction=auction)
        amount = args.aggregate(Max('bid_amount'))['bid_amount__max']
        if amount is None:
            amount = 0
        if float(bid_amount) < auction.start_bid or float(bid_amount) <= amount:
            # messages.warning(request, f'Your bid must be higher than: {max(amount, auction.start_bid)}!')
            message = f'Your bid must be higher than: {max(amount, auction.start_bid)}!'
            request.session["message"] = message
            return redirect("auction", pk=auction.id)

        bid = Bid.objects.create(
            auction=auction,
            user=request.user,
            bid_amount=bid_amount,
        )
        bid.save()
    return redirect("auction", pk=auction.id)


"""
@login_required
def own_auctions(request):
    # profile = Profile.objects.get(user=request.user)
    own_auctions = Auction.objects.filter(seller=request.user)
    
    favorites aka Observed
    
    did_bid = own_auction = bid.user
    recent = Auction.objects.filter(start_date=## descending max 10)
    ending = Auction.objects.filter(end_date=## descending max 10)
    observed = ##
    ended = Auction.objects.filter(active=False)
    
, 'did_bid': did_bid, 'recent': recent, 'ending': ending,
               'observed': observed, 'ended': ended
    

    context = {'auctions': own_auctions}
    return render(request, "auction/own_auctions.html", context)


@login_required
def favorites(request):
    profile = Profile.objects.get(id=request.user.id)
    favorites = profile.favorites.all()

    context = {'auctions': favorites}
    return render(request, "auction/favorites.html", context)
"""


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
