from django.db import models

class Brand(models.Model):
    Id = models.BigAutoField(primary_key=True)
    Brand_name = models.CharField(max_length=200)
    Quantity = models.BigIntegerField(default=0)

    def __str__(self):
        return self.Brand_name