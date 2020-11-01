from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("categories", views.categories, name="categories"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("all_listings", views.all_listings, name="all_listings"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove", views.remove, name="remove"),
    path("add_comment", views.add_comment, name="add_comment"),
]
