from django.views.generic import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from ..models import User, ProductReview, Product, Purchase
from ..forms import ReviewForm

@login_required
def purchases(request, user_id):
    purchases = request.user.purchases.all()
    return render(request, 'user_purchases.html', {'purchases': purchases})

@login_required
def review_product(request, user_id, purchase_id):
    purchase = Purchase.objects.get(id=purchase_id)
    if not purchase.reviewed:
        if request.method == 'GET':
            form = ReviewForm()
        elif request.method == 'POST':
            product_id = purchase.product.id
            form = ReviewForm(request.POST, product_id=product_id, user_id=user_id)
            if form.is_valid():
                form.save()
                purchase.reviewed = True
                purchase.save()
                return redirect('purchases', request.user.id)
        return render(request, 'product_review.html', {'form': form, 'purchase': purchase})
    else:
        raise Http404("Purchase already reviewed")