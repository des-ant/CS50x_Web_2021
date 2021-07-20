from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Listings
    listings = models.ForeignKey(Listing, related_name="creator")
    # Bids
    bids = models.ForeignKey(Bids, related_name="bidder")
    # Comments
    comments = models.ForeignKey(Comments, related_name="author")

    def __str__(self):
        return f"{self.id} {self.listings} {self.bids} {self.comments}"

# Model for auction listing
class Listing(models.Model):
    # User
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    # Title
    title = models.CharField(max_length=64)
    # Description
    description = models.TextField()
    # Starting Bid
    bid = models.DecimalField(decimal_places=2)
    # Image (Optional)
    image = models.ImageField()
    # Category
    # Date
    date = models.DateTimeField()
    
    def __str__(self):
        return f"{self.id}\n{self.title}\nDescription: {self.description}\nImage: {self.image}\nDate: {self.date}"

# Model for bids
class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    # Listing
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    # Price
    bid = models.DecimalField(decimal_places=2)
    # Date
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.id}\n{self.bid}\n{self.date}"

# Model for comments made on auction listings
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    # Comment
    comment = models.TextField()
    # Date
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.id}\n{self.comment}\n{self.date}"