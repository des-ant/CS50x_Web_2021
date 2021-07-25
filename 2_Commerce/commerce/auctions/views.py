from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category
from .forms import NewCategoryForm, NewListingForm


def index(request):
    # Show active listings on homepage
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
def new_listing(request):
    all_categories = Category.objects.all
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