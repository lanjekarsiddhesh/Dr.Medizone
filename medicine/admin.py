from django.contrib import admin
from .models import *

class Adminproduct(admin.ModelAdmin):
    list_display = ['Id','Image1','medicine_name', 'category','price','price_off','medicine_quantity','Total_medicines','uses','discription']

class adminCategory(admin.ModelAdmin):
    list_display = ['Id', 'Category']

class adminReview(admin.ModelAdmin):
    list_display = ['Id','product_img','rating','subject','review','patient','product','created_Date_at','created_Time_at']

class adminCart(admin.ModelAdmin):
    list_display = ['patient','total', 'is_paid']

class adminCartItem(admin.ModelAdmin):
    list_display = ['carts','Product','order', 'is_paid']

class adminOrder(admin.ModelAdmin):
    list_display = ['Orders_id','price','Cart','signature','is_paid','status','Date','Time']

class adminBrand(admin.ModelAdmin):
    list_display = ['Id','Brand_name','Quantity']

class adminwishlist(admin.ModelAdmin):
    list_display = ['patient','total']

class adminwishlistItem(admin.ModelAdmin):
    list_display = ['WishlistProduct','Product']


# Register your models here.
admin.site.register(Products,Adminproduct)
admin.site.register(Category,adminCategory)
admin.site.register(Reviews,adminReview)
admin.site.register(cart,adminCart)
admin.site.register(CartItem,adminCartItem)
admin.site.register(Orders,adminOrder)
admin.site.register(Brand,adminBrand)
admin.site.register(wishlist,adminwishlist)
admin.site.register(wishlistItem,adminwishlistItem)