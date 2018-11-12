from django.db import models
from .shop import Shop
from .options import Options
from .tags import Tags
from .productManager import ProductManager
from .categories import Categories
from PIL import Image
from ..search.searchProductDoc import ProductIndex
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
    # Relation with categories
    categories = models.ForeignKey(
        Categories, on_delete=models.CASCADE, null=True)
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

    def indexing(self):
        obj = ProductIndex(
            meta={'id': self.id},
            name=self.name,
            description=self.description,
            shop_name=self.shop_id.name,
            owner_name=self.shop_id.shop_owner.first_name,
            tags="".join(f"{tag.tags_name}, " for tag in self.tags.all())
        )
        obj.save()
        return obj.to_dict(include_meta=True)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
