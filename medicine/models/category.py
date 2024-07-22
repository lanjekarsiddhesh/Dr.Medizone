from django.db import models

class Category(models.Model):
    Id = models.AutoField(primary_key=True)
    Category = models.CharField(max_length=200)

    def __str__(self):
        return self.Category