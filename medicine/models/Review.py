from django.db import models
from .products import Products
from DMZ.models import Patient


class Reviews(models.Model):
    Id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, blank=True, null=True)
    patient = models.ForeignKey(Patient,on_delete=models.SET_NULL, blank=True, null=True)
    product_img = models.ImageField(upload_to='medicine_imgs/MedizoneShop/ReviewProduct')
    subject = models.CharField(max_length=500,default="")
    review = models.TextField(max_length=5000,blank=True)
    rating = models.FloatField()
    created_Time_at = models.TimeField(auto_now_add=True)
    created_Date_at = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.subject