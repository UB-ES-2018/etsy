from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden, JsonResponse
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required
from ..forms import RegisterForm, LoginForm, ShopForm, ProductForm, LogoUploadForm, ImageUploadForm, ProductUpdateForm, UpdateForm, ShopUpdateForm
from ..models import Product, Shop, User, UserFavouriteShop, UserFavouriteProduct, Address
from ..services import VariationsHandler, CartHandler, ProductImageHandler
from ..search.searchHandler import search_item, search_by_category
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.
def index(request):
	# Exclude products without creation finished
	first_10_products = Product.objects.filter(creation_finished = True).order_by('?')[:6]
	return render(request, 'home.html', {'first_10_products': first_10_products})

def shop_edit(request):
	return render(request, 'shop_edit_view.html', {})

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
def update_user_favourite_product(request, shop_id, product_id):
	if request.method == 'POST':
		product = Product.objects.get(id=product_id)
		fav = UserFavouriteProduct.objects.filter(user=request.user, product=product)
		if fav:
			fav.delete()
		else:
			UserFavouriteProduct.objects.create(user=request.user, product=product)
		return redirect('/shop/'+(str)(shop_id)+'/product/'+(str)(product_id))
	return HttpResponseForbidden('allowed only via POST')

@login_required
def user_avatar(request, user_id):
	if request.method == 'POST':
		form = LogoUploadForm(request.POST, request.FILES)
		if form.is_valid():
			request.user.profile_image = form.cleaned_data['image']
			request.user.save()
			return redirect('/profile/'+(str)(user_id))

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
			raise Http404('Unauthorized acces')
		
	return render(request, 'create_product.html', context)

def product(request, shop_id, product_id):
	context = {}
	try:
		product = Product.objects.get(id=product_id)
		context['product'] = product
		if (request.user.is_authenticated):
			fav = UserFavouriteProduct.objects.filter(user=request.user, product=product)
			context['is_favourite'] = True if fav else False
			
			if (Shop.objects.get(id=shop_id).shop_owner == request.user and not product.creation_finished):
				return redirect('product_images', shop_id = shop_id, product_id = product.id)
	except:
		raise Http404('This product does not exist')
		
	context['previews'] = Product.objects.exclude(id = product_id).filter(shop_id = shop_id, creation_finished = True).order_by('?')[:5]
	context['favs'] = len(UserFavouriteProduct.objects.filter(product = product))
	context['is_owner'] = request.user.is_authenticated and product.shop_id.shop_owner == request.user
	context['images'] = product.images.all().order_by('pk')
	
	if (not product.creation_finished):
		raise Http404('This product does not exist')
	
	return render(request, 'product_view.html', context)

@login_required
def product_images(request, shop_id, product_id):
	context = {}
	
	# Check that user is authenticated and is the owner of that shop
	if (request.user.is_authenticated and Shop.objects.get(id=shop_id).shop_owner == request.user):
		
		original_images = Product.objects.get(id=product_id).images.all().order_by('pk')
		
		if request.method == 'POST':
			form = ImageUploadForm(request.POST, request.FILES)
			
			if form.is_valid():
				
				for image_n in range(10):
					image = form.cleaned_data['image_' + str(image_n)]
					if image != None:
						if image_n < len(original_images):
							tmp = original_images[image_n]
							tmp.image = image
							tmp.save()
						else:
							ProductImageHandler.add_image_to_product(image, product_id)
						
				return redirect('product', shop_id = shop_id, product_id = product_id)
			
		# POST with errors or GET, render the form
		try:
			context['product'] = Product.objects.get(id=product_id)
			context['form'] = ImageUploadForm()
			context['shop_id'] = shop_id
			context['product_id'] = product_id
			context['images'] = original_images
		except:
			raise Http404('This product does not exist')
		
		return render(request, 'product_add_photos.html', context)
		
	else:
		raise Http404('Unauthorized acces')

@login_required
def product_image(request, product_id):
	if request.method == 'POST':
		form = ImageUploadForm(request.POST, request.FILES)
		
		if form.is_valid():
			for image_n in range(10):
				image = form.cleaned_data['image_' + str(image_n)]
				
				if image:
					ProductImageHandler.add_image_to_product(image, product_id)
			
			return JsonResponse({'Image added': 'ok'}, status=200)
		
		return JsonResponse({'errors': form.errors}, status=400)
	return JsonResponse({'error': 'Only post'}, status=400)

@login_required
def product_edit(request, shop_id, product_id):
	context = {}
	instance = Product.objects.get(id = product_id)
	instance_options = [(f.options_name) for f in instance.options.all()]
	
	if request.method == 'GET':
		# Get the product creation form
		# Populate the options
		options_initial = {f.name : (f.label in instance_options) for f in ProductForm().get_options_fields()}
		
		# Populate the tags
		tags_initial = {'tags' : ','.join([t.tags_name for t in instance.tags.all()])}
		
		# Join dictionaries
		initial = {**options_initial, **tags_initial}
		
		# Create the form
		context['form'] = ProductForm(instance = instance, initial=initial)
	
	elif request.method == 'POST':
		# Check that user is authenticated and is the owner of that shop
		if (request.user.is_authenticated and Shop.objects.get(id=shop_id).shop_owner == request.user):
			# Create a new product of that shop
			context['form'] = ProductUpdateForm(request.POST, shop_id = shop_id, product_id = product_id, instance = instance)
			
			if context['form'].is_valid():
				product = context['form'].save()
				shop_id = (str)(shop_id)
				
				return redirect('product_images', shop_id = shop_id, product_id = product.id)
			
		else:
			# TODO: Show error message properly
			return HttpResponse("Stop right there you criminal scum!")
		
	return render(request, 'edit_product.html', context)

@login_required
def shopping_cart(request):
	products = CartHandler.get_items_of_cart(request.user)
	total = CartHandler.get_total(request.user)
	return render(request, 'shopping_cart.html', {'products': products, 'total': total})


@login_required
def cart_action(request, action, product_id):
	if action == 'add':
		try:
			product = Product.objects.get(id=product_id)
			CartHandler.add_product_to_cart(request.user, product)
		except:
			raise Http404("Product does not exist")
	if action == 'remove':
		try:
			product = Product.objects.get(id=product_id)
			CartHandler.remove_product_from_cart(request.user, product)
		except: 
			raise Http404("Product does not exist")
	if action == 'amount':
		try:
			qty = request.GET.get('qty', 1)
			product = Product.objects.get(id=product_id)
			CartHandler.set_amount(request.user, product, qty)
		except: 
			raise Http404("Product does not exist")
	return redirect('cart')

@login_required
def checkout(request):
	CartHandler.create_purchases(request.user)
	return render(request, 'confirmation_view.html', {})

@login_required
def payment(request):
	return render(request, 'payment_view.html', {})

def search_results(request):
	search_query = request.GET.get('search_query', '')
	category_query = request.GET.get('category_query', None)
	min_price = request.GET.get('min_price', 0)
	max_price = request.GET.get('max_price', 99999999999)

	page = int(request.GET.get('page', '1'))

	if category_query:
		result = search_by_category(category_query, page, min_price=min_price, max_price=max_price)
	else:
		result = search_item(search_query, page, min_price=min_price, max_price=max_price)

	return render(request, 'search_results.html', {'results': result, 'query': search_query})

def category_results(request):
	search_query = request.GET.get('category_query', '')
	page = int(request.GET.get('page', '1'))

	result = search_by_category(search_query, page)

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

@login_required
def update_user(request, user_id):
	if request.method == 'GET':
		form = UpdateForm()
	if request.method == 'POST':
		form = UpdateForm(request.POST, request.FILES)
		if form.is_valid():
			request.user.first_name = form.cleaned_data['first_name']
			request.user.last_name = form.cleaned_data['last_name']
			zipcode = form.cleaned_data['zipcode']
			street = form.cleaned_data['street']
			country = form.cleaned_data['country']
			city = form.cleaned_data['city']
			try:
				request.user.address.zipcode = zipcode
				request.user.address.street = street
				request.user.address.country = country
				request.user.address.city = city
			except:
				adr = Address(zipcode,city,country,street)
				adr.save()
				request.user.address = adr
			request.user.save()
			return redirect('/profile/' + (str)(user_id))
	return render(request, 'profile_edit.html', {'form': form})

@login_required
def update_shop(request, shop_id):
	if request.method == 'GET':
		form = ShopUpdateForm()
	if request.method == 'POST':
		form = ShopUpdateForm(request.POST, request.FILES)
		if form.is_valid():
			shop = Shop.objects.get(id=shop_id)
			shop.language = form.cleaned_data['language']
			shop.country = form.cleaned_data['country']
			shop.currency = form.cleaned_data['currency']
			shop.save()
			return redirect('/shop/' + (str)(shop_id))
	return render(request, 'shop_edit_view.html', {'form': form})

def handler404(request, exception, template_name="404.html"):
    response = render_to_response("404.html")
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
