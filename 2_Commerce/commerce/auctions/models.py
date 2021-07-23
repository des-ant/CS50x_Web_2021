from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.id} {self.username} {self.first_name}"

# Allow listings to be sorted by category
class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

# Model for auction listing
class Listing(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE, related_name="catgory_items")
    date_created = models.DateTimeField()
    is_active = models.BooleanField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    
    def __str__(self):
        return f"{self.id} {self.creator} {self.title} {self.description} {self.image}"
        f"{self.category} {self.date_created} {self.is_active} {self.watchers}"

# Model for bids
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    price = models.DecimalField(max_digits=19, decimal_places=2)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.id} {self.user} {self.listing} {self.price} {self.date}"

# Model for comments made on auction listings
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    comment = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.id} {self.listing} {self.comment} {self.date}"

# Model for watchlist, allows users to save listings
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchers")
