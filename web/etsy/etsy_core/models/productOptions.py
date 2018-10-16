from django.db import models
from .product import Product
from .options import Options


class ProductOptions(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    options = models.ForeignKey(Options, on_delete=models.CASCADE)
