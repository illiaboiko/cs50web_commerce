from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.category




class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateField()
    end_time = models.DateField()
    # starting_bid = models.FloatField()
    # current_price = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="listing")
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="my_listings"
    )
    categories = models.ManyToManyField(Category, blank=True, related_name="listings")
    timestamp = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders", null=True, blank=True
    )

    def __str__(self):
        return self.title

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="watchlist"
    )

    def __str__(self):
        return f"User: {self.user.username} - Listing: {self.listing.title}"


class Comment(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"
