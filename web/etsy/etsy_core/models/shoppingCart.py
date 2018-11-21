from django.db import models
from .product import Product


class ShoppingCart(models.Model):
    id = models.AutoField(primary_key=True)
    items = models.ManyToManyField(Product, throught="ProductOnCart")


class ProductOnCart(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
