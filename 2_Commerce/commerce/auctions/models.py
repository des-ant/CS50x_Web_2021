from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    listings = models.ForeignKey(Listing, blank=True, related_name="creator")
    bids = models.ForeignKey(Bid, blank=True, related_name="bidder")
    comments = models.ForeignKey(Comment, blank=True, related_name="author")
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="watchers")

    def __str__(self):
        return f"{self.id} {self.listings} {self.bids} {self.comments} {self.watchlist}"

# Model for auction listing
class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField()
    category = models.ForeignKey(Category, related_name="catgory_items")
    date_created = models.DateTimeField()
    is_active = models.BooleanField()
    bids = models.ForeignKey(Bid, related_name="bid_listing")
    
    def __str__(self):
        return f"{self.id} {self.creator} {self.title} {self.description} {self.image}"
        f"{self.category} {self.date_created} {self.is_active} {self.bids}"

# Model for bids
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    price = models.DecimalField(decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.id} {self.user} {self.listing} {self.price} {self.date}"

# Model for comments made on auction listings
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    comment = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.id} {self.listing} {self.comment} {self.date}"

# Allow listings to be sorted by category
class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"