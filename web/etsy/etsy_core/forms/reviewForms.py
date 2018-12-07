from django import forms
from decimal import Decimal

from ..models import ProductReview, User, Product

import sys

class ReviewForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea, max_length=255, required=True)
    rating = forms.ChoiceField(required=True, choices=tuple((x, x) for x in range(6)))

    class Meta:
        model = ProductReview
        fields = ('description', 'rating')

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        print(rating, file=sys.stderr)
        rating = Decimal(f"{rating}.00")
        return rating
        
    def __init__(self, *args, **kwargs):
        self._product_id = kwargs.pop('product_id', None)
        self._user_id = kwargs.pop('user_id', None)
        if (self._user_id is not None):
            self._user = User.objects.get(id=self._user_id)
        if (self._product_id is not None):
            self._product = Product.objects.get(id=self._product_id)

        super(ReviewForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        review = super(ReviewForm, self).save(commit=False)
        review.user = self._user
        review.product = self._product

        if commit:
            review.save()

        return review