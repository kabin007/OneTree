from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('menu/',views.menu,name="menu"),
    path('login/',views.loginpage,name="login"),
    path('signup/',views.signuppage,name="signup"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('add2cart/<int:item_id>/',views.itemInfo,name="addCart"),
    path('products/',views.product,name="product"),
    path('add/',views.addFood,name="add"),
    path('foodcart/',views.foodcart,name="foodcart")
]