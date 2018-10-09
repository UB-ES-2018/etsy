from django import forms
from ..models import Product, Shop


class ProductForm(forms.ModelForm):
    name = forms.CharField(required=True)
    description = forms.CharField(required=True)

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

    def save(self, commit=True):
        product = super(ProductForm, self).save(commit=False)
        product.shop_id = self._shop
        if commit:
            product.save()
            self.save_m2m()
        return product
