from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import *
from .forms import *

from django.contrib.auth.decorators import login_required

from . import utils


def index(request):
    # check if the user if authenciated
    if request.user.is_authenticated:
        listings = Listing.objects.filter(is_active=True)
        watchlist_count = Watchlist.objects.filter(user=request.user).count()

        # Create a list to store triples of listings and their data
        listingData = []

        
        for listing in listings:
            # Check if the listing is in the user's watchlist
            in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
            # get current bid of a listing
            current_bid = listing.bids.last().amount

            # append the listing data to the list:
            listingData.append((listing, in_watchlist, current_bid))
        
        return render(
            request,
            "auctions/index.html",
            {
                "listings": listingData,
                "watchlist_count": watchlist_count,
            },
        )
    return render(request, "auctions/index.html")

@login_required(login_url="login")
def my_purchases(request):
    if request.method == "GET":
        user = request.user
        listings = Listing.objects.filter(winner=user)
        watchlist_count = Watchlist.objects.filter(user=request.user).count()
        
        # Create a list to store tuples of listings and their data
        listingData = []

        
        for listing in listings:
            # Check if the listing is in the user's watchlist
            in_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
            # get current bid of a listing
            current_bid = listing.bids.last().amount

            # append the listing data to the list:
            listingData.append((listing, in_watchlist, current_bid))
        
        return render(
            request,
            "auctions/my_purchases.html",
            {
                "listings": listingData,
                "watchlist_count": watchlist_count,
            },
        )
    else:
        return render(request, "auctions/index.html")


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            # get data for the new listing from POST object
            user = request.user
            title = request.POST["title"]
            description = request.POST["description"]
            starting_price = float(request.POST["current_price"])
            categories = request.POST.getlist("categories")
            image_url = request.POST["image_url"]

            # get Categories object from db
            categoriesData = Category.objects.filter(id__in=categories)
            
            # create new listing
            new_listing = Listing(
                title=title,
                seller=user,
                description=description,
                image_url=image_url,
            )
            new_listing.save()
            # update categories in the new listing
            new_listing.categories.set(categoriesData)

            # create new bid entry
            bid = Bid(user=request.user, amount=starting_price, listing=new_listing)
            bid.save()
            return HttpResponseRedirect(reverse("index"))
        

    elif request.method == "GET":
        watchlist_count = Watchlist.objects.filter(user=request.user).count()
        categoriesData = Category.objects.all()
        return render(
            request,
            "auctions/create_listing.html",
            {
                "categories": categoriesData,
                "watchlist_count": watchlist_count,
            },
        )


@login_required(login_url="login")
def listing(request, listing_id):
    if request.method == "GET":
        listing = Listing.objects.get(pk=listing_id)
        watchlist_count = Watchlist.objects.filter(user=request.user).count()
        in_watchlist = utils.is_listing_in_watchlist(request.user, listing_id)
        initial_price = listing.bids.first().amount
        latest_bid = listing.bids.last()
        bids_count = listing.bids.count()
        return render(
            request,
            "auctions/listing.html",
            {
                "listing": listing,
                "watchlist_count": watchlist_count,
                "in_watchlist": in_watchlist,
                "latest_bid": latest_bid,
                "initial_price": initial_price,
                "bids_count": bids_count,
            },
        )
    elif request.method == "POST":
        listing = Listing.objects.get(pk=request.POST["listing_id"])
        # TODO
        # figure out how to get the latest bid for a given lising
        current_bid = listing.bids.last().amount
        new_bid = float(request.POST["bid"])
        
        if new_bid > current_bid:
            bid = Bid(user=request.user, amount=new_bid, listing=listing)
            bid.save()
            
            messages.success(request, "Bid added")
            return redirect('listing', listing_id=listing_id)     
        else:
            messages.error(request, "Your bid must be greater than previous")
            return redirect('listing', listing_id=listing_id)     


@login_required(login_url="login")
def watchlist(request):
    if request.method == "GET":
        watchlist_entries = Watchlist.objects.filter(user=request.user)
        listings = [entry.listing for entry in watchlist_entries]
        watchlist_count = Watchlist.objects.filter(user=request.user).count()

        return render(
            request,
            "auctions/watchlist.html",
            {
                "listings": listings,
                "watchlist_count": watchlist_count,
            },
        )
    elif request.method == "POST":
        listing_id = request.POST["listing_id"]
        if listing_id:
            if request.POST["action"] == "add":
                listing = Listing.objects.get(pk=listing_id)
                entry = Watchlist(user=request.user, listing=listing)
                entry.save()
            elif request.POST["action"] == "remove":
                listing = Listing.objects.get(pk=listing_id)
                Watchlist.objects.filter(user=request.user, listing=listing).delete()
        return redirect('listing', listing_id=listing_id) 


@login_required(login_url="login")
def bid(request):
    if request.method == "POST":
        listing = Listing.objects.get(pk=request.POST["listing_id"])
        current_bid = listing.current_price.amount
        new_bid = float(request.POST["bid"])
        
        if new_bid > current_bid:
            bid = Bid(user=request.user, amount=new_bid)
            listing.current_price = bid
            message = utils.generate_message(code="success", message_text="Done!")
            
            return render(request, "auctions/apology.html", {
                "message": message,
            })
            
        else:
            message = utils.generate_message(code="danger", message_text="Unsussessful: your bid should be higher than the last bid")
            return render(request, "auctions/apology.html", {
                "message": message,
            })

    else:
        pass


@login_required(login_url="login")
def close_auction(request):
    if request.method == "POST":
        # get listing id from POST object
        listing_id = request.POST["listing_id"]
        # get listing entry
        listing = Listing.objects.get(pk=listing_id)
        # set the winner as a user who mande the bid the last and make the listing no longer active
        listing.winner = listing.bids.last().user
        listing.is_active = False
        # update listing field
        listing.save()
        return redirect('listing', listing_id=listing_id)
    else:
        return render(request, "auctions/index.html")
