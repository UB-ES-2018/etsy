from django.db import models


class ShoppingCart(models.Model):
    id = models.AutoField(primary_key=True)

class ProductOnCart(models.Model):
    cart = models.ForeignKey(ShoppingCart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    amount = models.IntegerField()
