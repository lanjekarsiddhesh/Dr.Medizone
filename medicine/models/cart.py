from django.db import models
from .products import Products
from DMZ.models import Patient

class cart(models.Model):
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name='carts')
    is_paid = models.BooleanField(default=False)
    total = models.FloatField(default=0)

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.Products.price)
        
        return sum(price)

class CartItem(models.Model):
    carts = models.ForeignKey(cart,on_delete=models.CASCADE,related_name="carItems")
    Product = models.ForeignKey(Products,on_delete=models.CASCADE,related_name="products")
    Qunatity = models.IntegerField(default=1)
    is_paid = models.BooleanField(default=False)
    order = models.CharField(max_length=500,null=True)
    
    def get_product_price(self):
        Price = [self.Product.price]
        return sum(Price)