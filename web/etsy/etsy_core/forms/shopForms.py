from django import forms

from ..models import Shop, User


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

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user', None)
        if (self._user is not None):
            User.objects.get(email=self._user.email)
        super(ShopForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        inst = super(ShopForm, self).save(commit=False)
        inst.shop_owner = self._user
        if (not self._user.has_shop):
            self._user.has_shop = True
            self._user.save()
        if commit:
            inst.save()
            self.save_m2m()
        return inst
