from django.db import models
from .products import Products
from DMZ.models import Patient

class wishlist(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='wish')
    total = models.FloatField(default=0)


class wishlistItem(models.Model):
    WishlistProduct = models.ForeignKey(wishlist,on_delete=models.CASCADE,related_name="Items")
    Product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="productItem")

    
    
    