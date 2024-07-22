from django.db import models
from .cart import cart

status_choice = (
    ("Order Received","Order Received"),
    ("Out For Delivery","Out For Delivery"),
    ("Order delivered","Order delivered"),
)


class Orders(models.Model):
    Orders_id = models.CharField(primary_key=True,max_length=500)
    Cart = models.ForeignKey(cart,on_delete=models.CASCADE,related_name='cart',null=True,blank=True)
    price = models.FloatField()
    signature = models.CharField(max_length=500,null=True)
    is_paid = models.BooleanField(default=False)
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=status_choice,default="Order Received")