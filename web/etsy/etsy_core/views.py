from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, ShopForm, ProductForm
from .models import Product, Shop
# Create your views here.


def index(request):
    return render(request, 'home.html', {})


def user_login(request):
    logout(request)
    redirect_to = request.POST.get('next', request.GET.get('next', '/'))
    redirect_to = (redirect_to
                   if is_safe_url(redirect_to, request.get_host())
                   else '/')
    if request.method == 'POST':
        # We save the previos page in order to redirect the user there if the login succeeds
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.cached_user)
            return HttpResponseRedirect(redirect_to)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form,
                                          'next': redirect_to})


def user_logout(request):
    logout(request)
    return redirect('index')


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data["password1"]
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'signup.html', {'form': form})


def shop(request, shop_id):
    return render(request, '', {})


@login_required
def create_shop(request):
    if request.method == 'POST':
        form = ShopForm(request.POST, user=request.user)
        if form.is_valid():
            shop = form.save()
            shop_id = shop.id
            # It should redirect to the shop_id
            return redirect('/shop/'+(str)(shop_id))
    else:
        form = ShopForm()
    return render(request, 'shop_creation.html', {'form': form})


@login_required
def create_product(request, shop_id):
    if request.method == 'GET':
        # Get the product creation form
        form = ProductForm()
    elif request.method == 'POST':
        # Check that user is authenticated and is the owner of that shop
        if (request.user.is_authenticated and Shop.objects.get(id=shop_id).shop_owner == request.user):
            # Create a new product of that shop
            form = ProductForm(request.POST, shop_id=shop_id)
            if form.is_valid():
                product = form.save()
                shop_id = (str)(shop_id)
                return redirect('index')
    return render(request, 'create_product.html', {'form': form})

def product(request, shop_id, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        product = None
    return render(request, 'product.html', {'product':product})