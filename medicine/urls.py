from django.contrib import admin
from django.urls import path
from . import views
# from django.conf import settings

#html file path here
urlpatterns = [
path("", views.index, name="Medicine"),
path("upload/", views.Upload, name="Product"),
path("deleteMedicine/<int:id>", views.deleteMedicine, name="deleteMedicine"),
path("product_details/<int:id>", views.product_details, name="Product"),
path("cart/", views.cart, name="Cart"),
path("add-to-cart/<int:id>/", views.add_to_cart, name="add_to_cart"),
path("add-to-wishlist/<int:id>/", views.add_to_wishlist, name="add_to_wishlist"),
path("RemoveCartitem/<int:id>", views.RemoveCartitem, name="RemoveCartitem"),
path("Mycart", views.Mycart, name="Mycart"),
path("Checkout", views.Checkout, name="Checkout"),
path("mSuccess/",views.success, name="success"),
path("Medicineproducts",views.MedicineproductPage,name='productPage')
]