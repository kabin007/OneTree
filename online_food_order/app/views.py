from django.shortcuts import get_object_or_404, render,redirect
from .forms import SignupForm,FoodForm
from django.contrib import messages
from django.contrib.auth import authenticate,login
from .models import Food,CartItem,Category

# Create your views here.

def home(request):
    foods=Food.objects.all()[:4]
    featured_food=Food.objects.filter(name__icontains='burger').first()
    categories=Category.objects.all()
    context={"food":foods,"featured_food":featured_food,"categories":categories}
    return render(request,'home.html',context)


def menu(request):
    foods=Food.objects.all()
    
    context={"food":foods}
    return render(request,'menu.html',context)

def dashboard(request):
    food_list=Food.objects.all()
    context={"food":food_list}
    return render(request,'admin_dashboard.html',context)


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

def signuppage(request):
    form=SignupForm() 
      #initialized the user creation form object and stored in the form variable
    #handling the input submit request
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



#views for add to cart section
def itemInfo(request,item_id):
    item=get_object_or_404(Food,id=item_id)

  
    if request.method=="POST":
        cart_item,created=CartItem.objects.get_or_create(
            user=request.user,
            product=item,
            quantity=request.POST.get('quantity'),
            )
        

    context={"item":item}
    return render(request,'product_detail.html',context)

def product(request):
    return render(request,'product_list.html')

def addFood(request):
    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES)
        if form.is_valid():
            food = form.save()
            return redirect('dashboard')
    else:
        form = FoodForm()
    return render(request, 'upload_food.html', {"form": form})


def updateFood(request):
    return render(request,"update_food.html")


def foodcart(request):
    cart_items=CartItem.objects.filter(user=request.user)
    context={"items":cart_items}
    return render(request,'cart.html',context)



