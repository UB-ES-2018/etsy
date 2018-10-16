from django.db import models
from .product import Product
from .tags import Tags

class ProductTags(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    tags = models.ForeignKey(Tags, on_delete=models.CASCADE)