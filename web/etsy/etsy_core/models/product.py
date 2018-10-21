from django.db import models
from .shop import Shop
from .options import Options
from .productManager import ProductManager


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name='product_name',
        max_length=50,
        null=False)

    description = models.CharField(
        verbose_name='product_description',
        max_length=255,
        null=False)

    # Relation with shop
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
    # Relation with options
    options = models.ManyToManyField(Options, through='ProductOptions')

    def __str__(self):
        return f"ID: {self.id} - PRODUCT: {self.get__name()}"

    # Our own properties
    def get__name(self):
        # The product is identified by its name
        return self.name

    # Our own properties
    def get__description(self):
        # The product is identified by its name
        return self.description

    objects = ProductManager()
