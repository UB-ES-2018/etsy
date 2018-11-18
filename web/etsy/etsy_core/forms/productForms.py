from django import forms
from ..models import Product, Shop, Options, Tags, ProductImage, Categories
from ..services import VariationsHandler


class ProductForm(forms.ModelForm):
    name = forms.CharField(required=True)
    description = forms.CharField(required=True)
    tags = forms.CharField(required=True)
    #categories = forms.CharField(required=True)
    first_image = forms.ImageField(label='first_image', required=False)
    second_image = forms.ImageField(label='second_image', required=False)
    third_image = forms.ImageField(label='third_image', required=False)

    class Meta:
        model = Product
        fields = ('name', 'description')

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
        categories = Categories.objects.filter(is_default=True)
        cats = []
        for category in categories:
            cats.append(f"category_{category.id}")
        self.fields['categories'] = forms.ChoiceField(choices=cats, required=True)

    def save(self, commit=True):
        product = super(ProductForm, self).save(commit=False)
        product.shop_id = self._shop

        if commit:
            product.save()
            self.update_options(product)
            self.update_tags(product)
            self.update_images(product)
            self.update_category(product)
            self.save_m2m()

        return product

    def get_options_fields(self):
        for field_name in self.fields:
            if field_name.startswith('option_'):
                yield self[field_name]

    def update_options(self, product):
        for field_name in self.fields:
            if field_name.startswith('option_') and self.cleaned_data.get(field_name):
                option_id = field_name.split('_')[1]
                variation = Options.objects.get(id=option_id)
                #product = Product.objects.get(id=product.id)
                VariationsHandler.add_variations_to_product(product, variation)

    def update_tags(self, product):
        tags = self.cleaned_data.get('tags')
        #product = Product.objects.get(id=product.id)
        for tag_name in tags.split(','):
            try:
                tag = Tags.objects.get(tags_name=tag_name)
            except:
                tag = Tags.objects.create(tags_name=tag_name)
            VariationsHandler.add_tag_to_product(product, tag)

    def update_images(self, product):
        image = self.cleaned_data.get('first_image', None)
        if image:
            ProductImage.objects.create(product=product, image=image)

        image = self.cleaned_data.get('second_image', None)
        if image:
            ProductImage.objects.create(product=product, image=image)

        image = self.cleaned_data.get('third_image', None)
        if image:
            ProductImage.objects.create(product=product, image=image)

    def update_category(self, product):
        category = self.cleaned_data.get('category', None)
        if category:
            product.categories = category

class ImageUploadForm(forms.Form):
    """Image upload form."""
    image = forms.ImageField()
