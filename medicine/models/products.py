from django.db import models
from .category import Category
from .brand import Brand

class Products(models.Model):
    Id = models.BigAutoField(primary_key=True)
    medicine_name = models.CharField(max_length=200)
    # company_name = models.CharField(max_length=200)
    medicine_quantity = models.CharField(max_length=200)
    Total_medicines = models.IntegerField()
    Expected_Total_medicines = models.IntegerField(default=1000)
    price = models.FloatField()
    price_off = models.CharField(max_length=200)
    discription = models.TextField()
    uses = models.TextField()
    Image1 = models.ImageField(upload_to='dmz_imgs/MedizoneShop/products')
    Image2 = models.ImageField(upload_to='dmz_imgs/MedizoneShop/products')
    Image3 = models.ImageField(upload_to='dmz_imgs/MedizoneShop/products')
    Image4 = models.ImageField(upload_to='dmz_imgs/MedizoneShop/products')
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, blank=True, null=True)
    company = models.ForeignKey(Brand,on_delete=models.CASCADE,blank=True,null=True)
    overall_rating = models.FloatField(default=0)

    def __str__(self):
        return self.medicine_name