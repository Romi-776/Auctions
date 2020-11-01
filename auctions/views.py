from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, auction_listing

# List of categories that we want to ask from users to choose from
categories_types = ['Furniture', 'Fashion', 'Electronics',
                    'Home Appliances', 'Books', 'Other']


# main page of the website on which all the active listings
# will be shown
def index(request):
    return render(request, "auctions/index.html", {
        # getting all the active listing from the DB in according to recent listing order
        "listings": auction_listing.objects.filter(active=True).order_by('added_when').reverse()
    })

# page to create an auction listing


def create_listing(request):
    ''' if the user had filled the form of creating a listing then do this '''
    if request.method == "POST":
        # create object using title, description and image_url given by the user
        Title = request.POST["title"]
        Des = request.POST["description"]
        url = request.POST["image_url"]
        category = request.POST["category"]

        listing = auction_listing(
            title=Title, description=Des, image_url=url, category=category, created_by=request.user.username)

        # saving that object to the DB
        listing.save()

        # Going to the updated index page
        return HttpResponseRedirect(reverse("index"))

    # Else give the user a form to fill to create a listing
    else:
        return render(request, "auctions/create.html", {
            "categories": categories_types
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def categories(request):
    # if the user came by filling up the form
    if request.method == "POST":

        # get the category give by the user
        choosen_category = request.POST["category"]

        # getting all the listings that belongs to the category
        # given by the user
        category_list = auction_listing.objects.filter(
            category=choosen_category, active=True).all()

        # returning to the category page showing all the listings
        # that belongs to that category
        return render(request, "auctions/categories.html", {
            "choosen_category": choosen_category,
            "category_list": category_list,
            "POST": 1
        })

    # else give the user to fill a form to choose a category
    # from which he wants to see the listings
    else:
        return render(request, "auctions/categories.html", {
            "categories": categories_types,
            "POST": 0
        })


# When anyone will click on any listing which is on the home page
# then this function will take the user to that listing's info page
def listing(request, listing_id):
    # getting the listing on which the user had clicked
    listing = auction_listing.objects.filter(id=listing_id).get()

    # Checking that by which method the user came to this place
    if request.method == "GET":
        # when user came by get method, i.e, by clicking on
        # a particular listing or filling the link to the search bar
        if listing:
            # then we're checking that the listing exists and
            # if it exists then show that listing
            return render(request, "auctions/listing.html", {
                "listing": listing
            })
        else:
            # otherwise show an Error
            return HttpResponse("Listing not found")

    # if the user came here by post method
    # it is only possible if the user had clicked on the
    # button of end listing
    else:
        # then make that listing inactive
        listing.active = False

        # update the listing's active status
        listing.save(update_fields=["active"])

        # show the remaining active listings on index page
        return HttpResponseRedirect(reverse("index"))


def all_listings(request):
    # getting all the listings sorted according to recent data
    listings = auction_listing.objects.order_by('added_when').reverse()

    return render(request, "auctions/all_listings.html", {
        "listings": listings
    })

# adding a listing to a user's watchlist or
# seeing all the watchlisted items of that user
def watchlist(request):
    # when the user clicks on add to watchlist button
    if request.method == 'POST':
        # then get the listing_id
        listing_id = request.POST['listing']

        # get the listing with that listing_id
        listing_obj = auction_listing.objects.get(id=listing_id)
        
        # add that listing to the watchlist of currently logged in user
        request.user.watchlist.add(listing_obj)

        # return the same page of that listing with a success message
        return render(request, "auctions/listing.html", {
            "listing": listing_obj, 
            "message": "Listing added to Watchlist",
        })
    # when the user clicks on watchlist button to see all
    # its watchlisted items
    else:
        # then return the list of all its watchlisted items
        return render(request, 'auctions/watchlist.html', {
            "watchlist": request.user.watchlist.all(),
        })

# remove an item from a particular user's watchlisted items.
def remove(request):
    # when user clicks on Remove from watchlist button
    if request.method == "POST":
        # get that listing's id
        listing_id = request.POST['listing']
        # get that listing with the previous id
        listing_obj = auction_listing.objects.get(id=listing_id)

        # remove that listing from the watchlist of the currently logged in user 
        request.user.watchlist.remove(listing_obj)

        # return the same listing page with a success message
        return render(request, "auctions/listing.html", {
            "listing": listing_obj,
            "message": "Listing removed from Watchlist",
        })
