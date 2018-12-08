from django import forms
from ..models import Product, Shop, Options, Tags, ProductImage, Categories
from ..services import VariationsHandler

	
class ProductForm(forms.ModelForm):
	name = forms.CharField(required=True)
	description = forms.CharField(required=True)
	tags = forms.CharField(required=True)
	categories = forms.ModelChoiceField(
		queryset=Categories.objects.filter(is_default=True), empty_label=None)
	price = forms.DecimalField(max_digits=8, decimal_places=2)

	class Meta:
		model = Product
		fields = ('name', 'description', 'categories', 'price')

	def clean_name(self):
		name = self.cleaned_data.get('name')
		qs = Product.objects.filter(name=name)
		if qs.exists():
			raise forms.ValidationError("Product name already taken")
		return name

	def __init__(self, *args, **kwargs):
		self._shop_id = kwargs.pop('shop_id', None)
		if (self._shop_id is not None):
			self._shop = Shop.objects.get(id=self._shop_id)
		super(ProductForm, self).__init__(*args, **kwargs)

		options = Options.objects.filter(is_default=True)
		for option in options:
			field_name = f"option_{option.id}"
			self.fields[field_name] = forms.BooleanField(required=False, label=f"{option.options_name}")

		self.fields['tags'].widget.attrs.update({
			'data-role': "tagsinput",
		})

	def save(self, commit=True):
		product = super(ProductForm, self).save(commit=False)
		product.shop_id = self._shop

		if commit:
			product.save()
			self.update_options(product)
			self.update_tags(product)
			self.save_m2m()

		return product

	def get_options_fields(self):
		for field_name in self.fields:
			if field_name.startswith('option_'):
				yield self[field_name]

	def update_options(self, product):
		VariationsHandler.remove_all_product_variations(product)
		
		for field_name in self.fields:
			if field_name.startswith('option_') and self.cleaned_data.get(field_name):
				option_id = field_name.split('_')[1]
				variation = Options.objects.get(id=option_id)
				VariationsHandler.add_variations_to_product(product, variation)

	def update_tags(self, product):
		VariationsHandler.remove_all_product_tags(product)
		
		tags = self.cleaned_data.get('tags')
		for tag_name in tags.split(','):
			try:
				tag = Tags.objects.get(tags_name=tag_name)
			except:
				tag = Tags.objects.create(tags_name=tag_name)
			VariationsHandler.add_tag_to_product(product, tag)


class ImageUploadForm(forms.Form):
	"""Image upload form."""
	
	# Adds 10 photos
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		for image_n in range(10):
				field_name = f"image_{image_n}"
				self.fields[field_name] = forms.ImageField(required=False)
			
	
class ProductUpdateForm(ProductForm):
	
	def __init__(self, *args, **kwargs):
		self._product_id = kwargs.pop('product_id', None)
		super().__init__(*args, **kwargs)
		
	
	def clean_name(self):
		# Check if another product has the same name
		name = self.cleaned_data.get('name')
		qs = Product.objects.exclude(id = self._product_id).filter(name = name)
		if qs.exists():
			raise forms.ValidationError("Product name already taken")
		return name
