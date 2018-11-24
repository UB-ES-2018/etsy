from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden, JsonResponse
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, ShopForm, ProductForm, LogoUploadForm, ImageUploadForm
from .models import Product, Shop, User, UserFavouriteShop
from .services import VariationsHandler, CartHandler, ProductImageHandler
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


def checkout(request):
	return render(request, 'confirmation_view.html', {})


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
		fav = UserFavouriteShop.objects.filter(user=request.user, shop=shop)
		is_favourite = True if fav else False
	except:
		raise Http404("Shop does not exist")
	return render(request, 'owners_shop.html', {'shop': shop, 'is_owner': is_owner, 'is_favourite': is_favourite})


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
def update_user_favourite_shop(request, shop_id):
	if request.method == 'POST':
		shop = Shop.objects.get(id=shop_id)
		fav = UserFavouriteShop.objects.filter(user=request.user, shop=shop)
		if fav:
			fav.delete()
		else:
			UserFavouriteShop.objects.create(user=request.user, shop=shop)
		return redirect('/shop/'+(str)(shop_id))
	return HttpResponseForbidden('allowed only via POST')


@login_required
def user_avatar(request, user_id):
	if request.method == 'POST':
		form = LogoUploadForm(request.POST, request.FILES)
		if form.is_valid():
			request.user.profile_image = form.cleaned_data['image']
			request.user.save()
			return redirect('/profile/'+(str)(user_id))


def product_image(request, product_id):
	if request.method == 'POST':
		form = ImageUploadForm(request.POST, request.FILES)
		
		if form.is_valid():
			ProductImageHandler.add_image_to_product(
				form.cleaned_data['image'], product_id)
			
			return JsonResponse({'Image added': 'ok'}, status=200)
		
		return JsonResponse({'errors': form.errors}, status=400)
	return JsonResponse({'error': 'Only post'}, status=400)


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
				return redirect('product_images', shop_id = shop_id, product_id = product.id)
			
		else:
			# TODO: Show error message properly
			return HttpResponse("Stop right there you criminal scum!")
		
	return render(request, 'create_product.html', context)

def product(request, shop_id, product_id):
	context = {}
	try:
		product = Product.objects.get(id=product_id)
		context['product'] = product
	except:
		raise Http404('This product does not exist')
	
	return render(request, 'product_view.html', context)

@login_required
def product_images(request, shop_id, product_id):
	context = {}
	try:
		context['product'] = Product.objects.get(id=product_id)
		context['form'] = ImageUploadForm()
		context['shop_id'] = shop_id
		context['product_id'] = product_id
	except:
		raise Http404('This product does not exist')
	
	return render(request, 'product_add_photos.html', context)

@login_required
def shopping_cart(request):
	products = CartHandler.get_items_of_cart(request.user)
	return render(request, 'shopping_cart.html', {'products': products})


@login_required
def cart_action(request, action, product_id):
	if action == 'add':
		try:
			product = Product.objects.get(id=product_id)
			CartHandler.add_product_to_cart(request.user, product)
		except:
			raise Http404("Product does not exist")

	return redirect('cart')


def search_results(request):
	search_query = request.GET.get('search_query', '')
	page = int(request.GET.get('page', '1'))

	result = search_item(search_query, page)

	return render(request, 'search_results.html', {'results': result, 'query': search_query})


def profile(request, user_id):
	try:
		user = User.objects.get(id=user_id)
		is_owner = False
		if (request.user.is_authenticated and user == request.user):
			is_owner = True
	except:
		raise Http404("User does not exist")

	return render(request, 'profile.html', {'user': user, 'is_owner': is_owner})
