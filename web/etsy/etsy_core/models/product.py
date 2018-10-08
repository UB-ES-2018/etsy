from django.db import models
from .shop import Shop
from .productManager import ProductManager

class Product(models.Model):
    name = models.CharField(
        verbose_name='product_name',
        max_length=50,
        null=False)
    
    #Creating a foreignKey
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.get__name())
    
    # Our own properties
    def get__name(self):
        # The shop is identified by its name
        return self.name

    objects = Pro