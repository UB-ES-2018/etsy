from django.db import models
from .shop import Shop
from .options import Options
from .tags import Tags
from .productManager import ProductManager
from PIL import Image
import os


def get_image_path(instance, filename):
    return os.path.join('product', str(instance.id), filename)


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
    # Relation with tags
    tags = models.ManyToManyField(Tags, through='ProductTags')

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

    def get_options_iter(self):
        for option in self.options.all():
            yield option

    objects = ProductManager()


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
