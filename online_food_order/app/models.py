from django.db import models
from django.contrib.auth.models import User

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

class CartItem(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Food,on_delete=models.CASCADE,default=1)
    quantity=models.IntegerField(default=1)
    added=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.product.name



class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    fullname=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    ward=models.CharField(max_length=100)
    area=models.CharField(max_length=100)
    mobile=models.CharField(max_length=20)

    def __str__(self):
        return f"{self.ward},{self.address},{self.area}, Mobile:{self.mobile}"



class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    items=models.ManyToManyField(CartItem)
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    payment_completed=models.BooleanField(default=False)

    def __str__(self):
        return f"Order ID:{self.id} made by {self.user.username}"

    
    def get_total(self):
        total=sum(items.product.price*items.quantity for items in self.items.all())
        self.total_amount=total
        self.save()

    def set_status(self,status):
        if status in dict(self.STATUS_CHOICES).keys():
            self.status=status
            self.save()