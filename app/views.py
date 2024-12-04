from django.shortcuts import get_object_or_404, render,redirect
from .forms import SignupForm,FoodForm,AddressForm
from django.contrib import messages
from django.contrib.auth import authenticate,login
from .models import Food,CartItem,Category,Address,Order
from django.db.models import Count,Sum,F
from django.http import JsonResponse
import logging
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
import stripe
from django.http import Http404
from django.conf import settings


# Create your views here.

#view for the home page / landing page
def home(request):
    foods=Food.objects.all()[:4]
    featured_food=Food.objects.filter(name__icontains='burger').first()
    featured_food_image=featured_food.food_image.url
    categories=Category.objects.all()
    context={"food":foods,"image":featured_food_image,"categories":categories,"featured_food":featured_food}
    return render(request,'home.html',context)


#view for the menu page
def menu(request):
    foods=Food.objects.all()
    context={"food":foods}
    return render(request,'menu.html',context)


#view for the admin dashboard page
def dashboard(request):
    food_list=Food.objects.all()
    context={"food":food_list}
    return render(request,'admin_dashboard.html',context)


#view for the login page
def loginpage(request):

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        #authenticating the user with the username and password
        user=authenticate(request,username=username,password=password)
      

        if user is not None:
                login(request,user)
                return redirect('home')
        else:
            messages.info(request,'Username or Password doesnt exist!!')


    return render(request,'login.html')


#view for the signup page
def signuppage(request):
    form=SignupForm() 
 
    if request.method=='POST':
        #populate the empty user creation form
        form=SignupForm(request.POST) 

        #check if the populated user creation form is valid
        if form.is_valid():
            user=form.cleaned_data.get('username')
            form.save()
            messages.success(request,'Account created Successfully for'+" " +user)
            return redirect('login')

    context={"form":form}
    return render(request,'signup.html',context)



#view for the item detail page
def itemInfo(request,item_id):
    item=get_object_or_404(Food,id=item_id)

    if request.method=="POST":
        cart_item,created=CartItem.objects.get_or_create(
            user=request.user,
            product=item,
            quantity=request.POST.get('quantity'),
            )

        if not created:
            cart_item.quantity+=1
            cart_item.save()
        

    context={"item":item}
    return render(request,'product_detail.html',context)


#view for the product that needs to be listed in the admin dashboard
def product(request):
    return render(request,'product_list.html')


#view to add food items from the admin dashboard panel
def addFood(request):
    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save()
            return redirect('dashboard')
    else:
        form = FoodForm()
    return render(request, 'upload_food.html', {"form": form})


#view to update food from the admin dashboard panel
def updateFood(request,food_id):
   food=get_object_or_404(Food,id=food_id)

   if request.method=="POST":
        form=FoodForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')


        return render(request,"update_food.html",{"form":form})


#view for the cart page
def foodcart(request):
    '''
    corresponds to the sql statement 'SELECT * FROM CartItem WHERE user=user'
    --returns a query set
    '''
    items=CartItem.objects.filter(user=request.user)
    cart_total=sum(cart_items.product.price*cart_items.quantity for cart_items in items)
    total_items=sum(items.quantity for items in items)
    context={'cart_total':cart_total,'total_items':total_items,'items':items}

    return render(request,'cart.html',context)



#view to handle increment functionality of  the quantity of the Cartitem

def increment_quanity(request,item_id):
    item=CartItem.objects.get(user=request.user,id=item_id)
    quantity=item.quantity

    if quantity>=0:
        quantity+=1
        CartItem.objects.filter(id=item.id).update(quantity=quantity)

    return redirect('foodcart')


#view to handle the decrement functionality of the quantity of the Cartitem
def decrement_quantity(request,item_id):
    item=CartItem.objects.get(user=request.user,id=item_id)
    quantity=item.quantity

    if quantity>=0:
        quantity-=1
        CartItem.objects.filter(id=item.id).update(quantity=quantity)

    return redirect('foodcart')

#view to handlle the functionality to remove the item from the cartItem
def remove_item(request,item_id):
    cart_item=CartItem.objects.get(id=item_id,user=request.user)
    cart_item.delete()

    return redirect('foodcart')


def talk_with_ai(request):
    return render(request,'chatbot.html')


def add_to_cart(request,item_id):
    item=get_object_or_404(Food,id=item_id)
    cart_item,created=CartItem.objects.get_or_create(
        user=request.user,
        product=item
    )

    if not created:
        CartItem.objects.filter(user=request.user, product=item).update(quantity=F('quantity') + 1)


    return redirect('menu')


def about(request):
    return render(request,'about_us.html')


def checkoutPage(request,order_id):
        try:
            order=Order.objects.get(id=order_id,user=request.user)

            items=order.items.all()

            context={
                'order_id':order_id,
                'items':items,
                'address':order.address,
                'total_amount':order.total_amount,
                'status':order.status,
                'created':order.created,
                'updated':order.updated,
                'payment':order.payment_completed
            }

            return render(request,'checkout.html',context)
        
        except Order.DoesNotExist:
            messages.error(request,'Order Does not exist for the user')
            return redirect('foodcart')


def payment(request,order_id):
    order=Order.objects.get(id=order_id)
    total_amount=order.total_amount
    context={"total":total_amount,"order_id":order.id}
    return render(request,'payment.html',context)

def update_address(request):
  if request.method == "POST":
    # Get the data from the POST request
    fullname = request.POST.get('fullname')
    address_value= request.POST.get('address')
    ward = request.POST.get('ward')
    area = request.POST.get('area')
    mobile = request.POST.get('mobile')

    try:
        # Retrieve the existing address for the user
        address = Address.objects.get(user=request.user)
        
        # Update the fields
        address.fullname = fullname
        address.address = address_value
        address.ward = ward
        address.area = area
        address.mobile = mobile

        # Save the updated address
        address.save()
        return redirect('payment')

    except Address.DoesNotExist:
        # If the user doesn't have an address, create a new one
        address = Address(
            user=request.user,
            fullname=fullname,
            address=address_value,
            ward=ward,
            area=area,
            mobile=mobile
        )
        address.save()
        return redirect('payment')

  return render(request, 'update_address.html')



#view to handle the order processing
def process_order(request):
    if request.method=="POST":
        cart_item=CartItem.objects.filter(
            user=request.user,
            )
    
        address,created=Address.objects.get_or_create(user=request.user)
        if created:
            messages.warning(request,'Please update your address')
            return redirect('update_address')

            
        total_amount=sum(items.product.price*items.quantity for items in cart_item)

        order=Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            address=address,
            status='Pending'
            )
        #adding the cart items to the order
        order.items.set(cart_item)

        messages.success(request,f"Order: {order.id} has been placed successfully.")
        return redirect(reverse('checkout', args=[order.id]))
    
    return redirect('cart.html')

def service(request):
    return render(request,'services.html')

def direct_order(request, item_id):
    if request.method == 'POST':
        # Get the food item and add it to the cart
        item = get_object_or_404(Food, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=item
        )
        
        # Get or create the user's address
        address, created = Address.objects.get_or_create(user=request.user)
        if created:
            messages.warning(request, 'Please update your address')
            return redirect('update_address')
        
      
        total_amount = item.price

        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_amount=total_amount,
            address=address,
            status='Pending'
        )

        # Add cart items to the order (ensure `cart_item` is in an iterable)
        order.items.add(cart_item)

        # Prepare context if you need to render a template (not needed for redirect)
        context = {
            'order_id': order.id,
            'items': order.items.all(),
            'address': order.address,
            'total_amount': order.total_amount,
            'status': order.status,
            'created': order.created,
            'updated': order.updated,
            'payment': order.payment_completed
        }

        # Redirect to the checkout page with `order_id` as a URL parameter
        return redirect(reverse('checkout', args=[order.id]))
    
    # Fallback redirect if the request method is not POST
    return redirect('menu')  # Replace 'food_menu' with an appropriate fallback URL




def admin_dashboard(request):
    # Fetch and manage orders here
    orders = Order.objects.all()  # Example: retrieving all orders
    return render(request, 'admin_dashboard.html', {'orders': orders})


def remove_order(request, order_id):
    order = Order.objects.filter(id=order_id)
    if order.exists():
        order.delete()
        print("Order deleted successfully.")
    else:
        print("Order not found.")
    return redirect('dashboard')

def modify_order(request,order_id):
    pass



stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def initiate_payment(request, order_id):
    # Fetch the order details using the order_id
    order = get_object_or_404(Order, id=order_id)
    
    # Create a Stripe checkout session with dynamic order data
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',  # Set currency as per your needs
                'product_data': {
                    'name': f'Order {order.id}',  # Use order ID for identification
                },
                'unit_amount': int(order.total_amount * 100),  # Stripe uses cents, so multiply by 100
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url="http://127.0.0.1:8000/payment-success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://127.0.0.1:8000/payment-cancel",
        client_reference_id=str(order.id)
    )
    

    # Redirect the user to the Stripe checkout page
    return redirect(session.url)

def payment_success(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        raise Http404("Session ID not found")

    # Retrieve session details from Stripe
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        order_id = session.client_reference_id  # Adjust based on your setup
        order = get_object_or_404(Order,id=order_id)
        
        #update the payment status of the order to True
        order.payment_completed = True
        order.save()
    except stripe.error.StripeError:
        raise Http404("Could not retrieve session")

    # You can access various session details here
    context = {
        'session_id': session.id,
        'amount_total': session.amount_total / 100,  # Amount in the currency's main unit
        'customer_email': session.customer_details.email,
        'payment_status': session.payment_status,
    }

    return render(request, 'payment_success.html', context)

def search(request):
    query = request.GET.get('q', '')
    results = Food.objects.filter(name__icontains=query)
    results_list = [{'id': item.id, 'name': item.name,'image':item.food_image.url,'price':item.price} for item in results]
    return JsonResponse(results_list, safe=False)