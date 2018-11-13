from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, ShopForm, ProductForm, LogoUploadForm, ImageUploadForm
from .models import Product, Shop
from .services import VariationsHandler
from .search.searchHandler import search_item
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
        if request.user.is_authenticated:
            return redirect('index')
    return render(request, 'signup.html', {'form': form})


def shop(request, shop_id):
    try:
        shop = Shop.objects.get(id=shop_id)
        is_owner = False
        if (request.user.is_authenticated and Shop.objects.get(id=shop_id).shop_owner == request.user):
            is_owner = True
    except:
        raise Http404("Shop does not exist")
    return render(request, 'owners_shop.html', {'shop': shop, 'is_owner': is_owner})


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
def shop_logo(request, shop_id):
    if request.method == 'POST':
        shop = Shop.objects.get(id=shop_id)
        form = LogoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            shop = request.user.shop
            shop.shop_profile_image = form.cleaned_data['image']
            shop.save()
            return redirect('/shop/'+(str)(shop_id))
        return HttpResponseForbidden(form.errors)
    return HttpResponseForbidden('allowed only via POST')


@login_required
def product_image(request,shop_id,product_id, img_num):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            if img_num == 1:
                product.first_image= form.cleaned_data['image']
            elif (img_num == 2):
                product.second_image = form.cleaned_data['image']
            else:
                product.third_image = form.cleaned_data['image']
            product.save()
            return redirect('/shop/'+(str)(shop_id)+'/product/'+(str)(product_id))
        return HttpResponseForbidden(form.errors)
    return HttpResponseForbidden('allowed only via POST')


@login_required
def create_product(request, shop_id):
    context = {}
    if request.method == 'GET':
        # Get the product creation form
        context['form'] = ProductForm()
        context['basic_variations'] = VariationsHandler.get_default_variations()
    elif request.method == 'POST':
        # Check that user is authenticated and is the owner of that shop
        if (request.user.is_authenticated and Shop.objects.get(id=shop_id).shop_owner == request.user):
            # Create a new product of that shop
            context['form'] = ProductForm(request.POST, shop_id=shop_id)
            if context['form'].is_valid():
                product = context['form'].save()
                shop_id = (str)(shop_id)
                return redirect('index')
    return render(request, 'create_product.html', context)


def product(request, shop_id, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        raise Http404('This product does not exist')
    return render(request, 'product_view.html', {'product': product})


def search_results(request):
    search_query = request.GET.get('search_query', '')
    page = int(request.GET.get('page', '1'))

    result = search_item(search_query, page)

    return render(request, 'search_results.html', {'results': result})


def profile(request, user_id):
    # TODO
    return render(request, 'profile.html')
