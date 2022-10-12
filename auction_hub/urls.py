"""auction_hub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import auction.views
import profiles.views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", auction.views.home, name="home"),

    # Accounts
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),

    # Category
    path('category/<str:pk>/', auction.views.category, name="category"),
    path('categories/', auction.views.categories, name='categories'),
    # Auction
    path('auction/<str:pk>/', auction.views.auction, name='auction'),
    path('auctions/', auction.views.auctions, name='auctions'),
    # Profile
    path('createprofile/', profiles.views.create_profile, name='create_profile'),
    path('user/<pk>', profiles.views.user_profile, name='profile'),
    path('edituser/', profiles.views.edit_profile, name='edit_profile'),
    path('users/', profiles.views.profiles_list, name='profiles'),
    # Rating
    #path('ratings/', auction.views.ratings, name='ratings'),
    # Favorites
    path('favorites/', auction.views.favorites, name='favorites'),
    path('remove_favorites/<id_item>', auction.views.remove_favorites, name='remove_favorites'),
    path('add_favorites/<id_item>', auction.views.add_favorites, name='add_favorites'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
