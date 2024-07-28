from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category= models.CharField(max_length=64)
  
    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE,  blank=True, null = True , related_name="user")
    price = models.FloatField()
    updated_price= models.FloatField(default=0)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=1000)
    active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True,null=True, related_name="watch_user")
    category= models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null = True ,related_name="categoryname")

    def __str__(self):
        return f"Title: {self.title} by {self.owner}"

class  Bids(models.Model):
    auction= models.ForeignKey(Listing, on_delete=models.CASCADE,  blank=True, null = True , related_name="bidlisting")
    bid= models.FloatField(default=0)
    buyer= models.ForeignKey(User, on_delete=models.CASCADE,  blank=True, null = True , related_name="listingbuyer")

    def __str__(self):
        return f"{self.buyer} on {self.auction}"
    

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  blank=True, null = True , related_name="writer")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,  blank=True, null = True , related_name="lisitngcomment")
    comment= models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"{self.user} on {self.listing}"
