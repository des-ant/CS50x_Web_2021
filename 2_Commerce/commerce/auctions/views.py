from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count, Sum, Case, When, IntegerField
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Listing, Category, Comment
from .forms import NewCategoryForm, NewListingForm, NewBidForm, NewCommentForm


def index(request):
    # Show active listings on homepage
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "title": "Active Listings",
        "empty": "No active listings to display"
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


# View for creating new listing
@login_required
def new_listing(request):
    all_categories = Category.objects.all
    # Load forms
    listing_form = NewListingForm()
    category_form = NewCategoryForm()
    context = {
        "listing_form": listing_form,
        "category_form": category_form,
        "all_categories": all_categories
    }
    if request.method == "POST":
        # Split form data by model attributes
        category_keys = ["name"]
        listing_keys = ["title", "description", "price", "image"]
        # Function to split data into separate dictionaries based on keys
        filter_by_key = lambda keys: {x: request.POST[x] for x in keys}
        category_data = filter_by_key(category_keys)
        listing_data = filter_by_key(listing_keys)
        # Get category id if category exists, compare using TitleCase
        category_input = category_data["name"].title()
        category = Category.objects.filter(name=category_input).first()
        # No match found, create new category
        if category is None:
            category_data["name"] = category_input
            category_form = NewCategoryForm(category_data)
            # If category form data is valid, create new category and add it to
            # listing form data
            if category_form.is_valid():
                category = category_form.save()
            else:
                return render(request, "auctions/newlisting.html", context)
        # Check if listing form data is valid
        listing_form = NewListingForm(listing_data)
        if listing_form.is_valid():
            new_listing_object = listing_form.save(commit=False)
            # Autofill attributes of new listing objects
            new_listing_object.creator = request.user
            new_listing_object.category = category
            new_listing_object.date_created = datetime.now()
            new_listing_object.is_active = True
            new_listing_object.save()
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/newlisting.html", context)
    return render(request, "auctions/newlisting.html", context)


# View for each individual listing
def listing(request, listing_id):
    # Return 404 page if listing not found
    listing_obj = get_object_or_404(Listing, pk=listing_id)
    # Get bid form and pass it to html template
    bid_form = NewBidForm()
    bidder_count = listing_obj.listing_bids.count()
    # Get information about highest bid
    highest_bid = listing_obj.highest_bid
    highest_bidder = None
    highest_bid_price = None
    if highest_bid:
        highest_bidder = highest_bid.user
        highest_bid_price = highest_bid.price
    # Check if listing is part of user's watchlist
    watching = False
    if request.user.is_authenticated and request.user.watchlist.filter(pk=listing_id):
        watching = True
    # Get comment data and pass it to html template
    listing_comments = listing_obj.listing_comments.all()
    # Get comment form and pass it to html template
    comment_form = NewCommentForm()
    # Check that user is creator of listing
    is_creator = False
    if request.user == listing_obj.creator:
        is_creator = True
    context = {
        "listing": listing_obj,
        "bid_form": bid_form,
        "bidder_count": bidder_count,
        "highest_bidder": highest_bidder,
        "highest_bid_price": highest_bid_price,
        "watching": watching,
        "comment_form": comment_form,
        "listing_comments": listing_comments,
        "is_creator": is_creator
    }
    if request.method == "POST":
        # Check if bid form received
        if "price" in request.POST:
            bid_form = NewBidForm(request.POST)
            # Check bid form data is valid
            if bid_form.is_valid():
                # Make sure bid price is higher than current bid
                bid_price = bid_form.cleaned_data["price"]
                min_bid = listing_obj.price
                # Compare to starting price if no bid placed yet
                if listing_obj.highest_bid:
                    min_bid = listing_obj.highest_bid.price
                if bid_price <= min_bid:
                    messages.error(request, "Error: bid must be higher than current price")
                    return render(request, "auctions/listing.html", context)
                # Bid is valid, autofill attributes then save new bid
                new_bid_object = bid_form.save(commit=False)
                new_bid_object.user = request.user
                new_bid_object.listing = listing_obj
                new_bid_object.date = datetime.now()
                new_bid_object.save()
                # Update highest bid on listing object
                listing_obj.highest_bid = new_bid_object
                listing_obj.save()
                return HttpResponseRedirect(reverse("auctions:listing", args=[listing_id]))
            else:
                messages.error(request, "Error: invalid bid")
                return render(request, "auctions/listing.html", context)
        # Check if comment form received
        elif "comment" in request.POST:
            comment_form = NewCommentForm(request.POST)
            # Check comment form data is valid
            if comment_form.is_valid():
                # Comment is valid, autofill attributes then save new comment
                new_comment_object = comment_form.save(commit=False)
                new_comment_object.user = request.user
                new_comment_object.listing = listing_obj
                new_comment_object.date = datetime.now()
                new_comment_object.save()
                return HttpResponseRedirect(reverse("auctions:listing", args=[listing_id]))
            else:
                messages.error(request, "Error: invalid comment")
                return render(request, "auctions/listing.html", context)
    return render(request, "auctions/listing.html", context)


# Add or remove from watchlist
def watch(request, listing_id):
    # Return 404 page if listing not found
    listing_obj = get_object_or_404(Listing, pk=listing_id)
    # Remove listing if found in watchlist
    watchlisting = request.user.watchlist.filter(pk=listing_id).first()
    if watchlisting:
        request.user.watchlist.remove(watchlisting)
    else:
        # Add to watchlist if not already added
        request.user.watchlist.add(listing_obj)
    return listing(request, listing_id)


# Show all listings from user's watchlist
def watchlist(request):
    watchlistings = request.user.watchlist.all()
    context = {
        "listings": watchlistings
    }
    return render(request, "auctions/watchlist.html", context)


# List all categories of listings
def categories(request):
    # Count number of active listings per Category
    count_active_categories = Category.objects.annotate(
        num_items=Sum(
            Case(
                When(category_items__is_active=True, then=1),
                default=0,
            ),
            output_field=IntegerField()
        )
    )
    context = {
        "categories": count_active_categories
    }
    return render(request, "auctions/categories.html", context)


# View all active listings in a category
def category(request, category_id):
    # Return 404 page if category not found
    category_obj = get_object_or_404(Category, pk=category_id)
    # Filter listings by category
    listings = category_obj.category_items.all()
    context = {
        "listings": listings,
        "title": f"Active Listings for Category: {category_obj.name}",
        "empty": f"No active listings to display for Category: {category_obj.name}"
    }
    return render(request, "auctions/index.html", context)


# Close listing
def close_listing(request, listing_id):
    # Return 404 page if listing not found
    listing_obj = get_object_or_404(Listing, pk=listing_id)
    # Check that user is creator of listing
    if request.user == listing_obj.creator:
        listing_obj.is_active = False
        listing_obj.save()
    else:
        # User is not creator of listing
        messages.error(request, "Error: must be creator to close listing")
    return listing(request, listing_id)