from django.db import models
from .product import Product
from .categories import Categories


class ProductCategories(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE)
