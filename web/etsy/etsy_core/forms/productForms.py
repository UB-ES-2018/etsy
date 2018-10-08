from django import forms
from ..models import Product, User


class ProductForm(forms.ModelForm):
    name = forms.CharField(required=True)
        
    forms.ModelMultipleChoiceField(
        choices=[(shop.shop_owner, shop.name) for shop in Shop.objects.all().filter(name=self._user)],
        widget=forms.HiddenInput(),
        required=True)

    class Meta:
        model = Shop
        fields = ('name', 'shop_id')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = Product.objects.filter(name=name)
        if qs.exists():
            raise forms.ValidationError("Product name already taken")
        return name

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)
    