from django.contrib import admin
from .models import Food,Category,CartItem,Address,Order

# Register your models here.
admin.site.register(Food)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Address)
admin.site.register(Order)

