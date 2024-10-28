from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('menu/',views.menu,name="menu"),
    path('login/',views.loginpage,name="login"),
    path('signup/',views.signuppage,name="signup"),
    path('dashboard/',views.admin_dashboard,name="dashboard"),
    path('add2cart/<int:item_id>/',views.itemInfo,name="addCart"),
    path('add-to-cart/<int:item_id>/',views.add_to_cart,name="addCart2"),
    path('products/',views.product,name="product"),
    path('add/',views.addFood,name="add"),
    path('foodcart/',views.foodcart,name="foodcart"),
    path('update/<int:food_id>/',views.updateFood,name="update"),
    path('decrement/<int:item_id>/',views.increment_quanity,name="increment"),
    path('increment/<int:item_id>/',views.decrement_quantity,name="decrement"),
    path('remove-item/<int:item_id>/',views.remove_item,name="remove_item"),
    path('about-us/',views.about,name="about"),
    path('checkout/<int:order_id>/',views.checkoutPage,name="checkout"),
    path('update_address',views.update_address,name="update_address"),
    path('initiate_payment/<int:order_id>/',views.initiate_payment,name="initiate_payment"),
    path('process-order/',views.process_order,name="process_order"),
    path('services/',views.service,name="service"),
    path('ordernow/<int:item_id>/',views.direct_order,name="direct_order"),
    path('delete_order/<int:order_id>/',views.remove_order,name="delete_order"),
    path('edit_order/<int:item_id>/',views.modify_order,name="edit_order"),
    path('payment-success/',views.payment_success,name="success"),
    path('payment/<int:order_id>/',views.payment,name="payment")
]