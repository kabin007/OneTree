from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField()
    category_image=models.ImageField(blank=True,null=True,upload_to="images/")

    def __str__(self):
        return self.name
    


class Food(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(max_digits=6,decimal_places=2)
    rating=models.DecimalField(max_digits=6,decimal_places=2)
    category_name=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    delivery_time=models.IntegerField()
    food_image=models.ImageField(null=True,blank=True,upload_to="images/")
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


class  CartItem(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.IntegerField()
    delivery_time=models.CharField(max_length=100)
    added=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product_name


