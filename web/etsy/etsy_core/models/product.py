from django.db import models
from .shop import Shop
from .options import Options
from .tags import Tags
from .productManager import ProductManager
from .categories import Categories
from PIL import Image
from ..search.searchProductDoc import ProductIndex
from ..search.searchHandler import create_elastic_connection
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

    price = models.DecimalField(max_digits=8, decimal_places=2)
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
    
    def get_tags_iter(self):
        for tag in self.tags.all():
            yield tag

    objects = ProductManager()

    def indexing(self):
        create_elastic_connection()
        
        string_tags = ""
        for tag in self.get_tags_iter():
            string_tags += f", {tag.tags_name}"
        
        obj = ProductIndex(
            meta={'id': self.id},
            name=self.name,
            description=self.description,
            shop_name=self.shop_id.name,
            owner_name=self.shop_id.shop_owner.first_name,
            tags=string_tags,
            category= self.categories.category_name if self.categories else None,
            price=self.price
        )
        obj.save()
        return obj.to_dict(include_meta=True)

    def get_first_image(self):
        if (self.images.count() is not 0):
            if self.images.all()[0].image:
                return self.images.all()[0].image.url
        return "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQuNrn-6eMLGpA5KOhqSwxOdAT6VKbjkBNbNIYodQHqj1hJC1Hf"

    def get_reviews(self):
        if (len(self.reviews.all())):
            total = 0
            for review in self.reviews.all():
                total += review.rating
            percent = int((float(total/len(self.reviews.all()))/5.0) * 100)
            return (percent, len(self.reviews.all()))
        else:
            return "empty"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
