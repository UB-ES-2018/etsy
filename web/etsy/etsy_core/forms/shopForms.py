from django import forms

from ..models import Shop


class ShopForm(forms.ModelForm):
    name = forms.CharField()
    ## Options for the choice fields pending to add##
    language = forms.ChoiceField(choices=[(1, 'ES'), (2, 'EN')])
    country = forms.ChoiceField(choices=[(1, 'ES'), (2, 'UK')])
    currency = forms.ChoiceField(choices=[(1, 'EUR'), (2, 'GBP')])

    class Meta:
        model = Shop
        fields = ('name', 'language', 'country', 'currency')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = Shop.objects.filter(name=name)
        if qs.exists():
            raise forms.ValidationError("Shop name already taken")
        return name
