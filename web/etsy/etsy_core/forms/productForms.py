from django import forms
from ..models import Product, User


class ProductForm(forms.ModelForm):
    name = forms.CharField(required=True)
        
    forms.ModelMultipleChoiceField(
        widget=forms.HiddenInput(), required=False, queryset=User.objects.a)

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
        super(ProductForm, self).__init__(*args, **kwargs)
