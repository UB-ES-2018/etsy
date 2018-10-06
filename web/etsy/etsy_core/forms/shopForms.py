from django import forms

from ..models import Shop

class RegisterForm(forms.ModelForm):
    name = forms.CharField(widget=forms.CharField)
    ## Options for the choice fields pending to add##
    language = forms.ChoiceField()
    country = forms.ChoiceField()
    currency = forms.ChoiceField()

    class Meta:
        model = Shop
        fields = ('name',)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = Shop.objects.filter(name=name)
        if qs.exists():
            raise forms.ValidationError("Shop name already taken")
        return name


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user