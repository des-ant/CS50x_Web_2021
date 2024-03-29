from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.id} {self.username} {self.first_name}"

# Allow listings to be sorted by category
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

# Model for auction listing
class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True, upload_to="auctions")
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE, related_name="category_items")
    date_created = models.DateTimeField()
    is_active = models.BooleanField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    highest_bid = models.ForeignKey('Bid', null=True, blank=True, on_delete=models.CASCADE, related_name="winners")
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    
    def __str__(self):
        return f"{self.id} {self.creator.username} {self.title} {self.is_active} {self.price}"

# Model for bids
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    price = models.DecimalField(max_digits=19, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.id} {self.user.username} {self.listing} {self.price}"

# Model for comments made on auction listings
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    comment = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.id} {self.user.username} {self.listing.id} {self.comment}"
