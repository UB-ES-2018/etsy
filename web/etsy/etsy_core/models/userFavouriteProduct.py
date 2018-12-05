from django.db import models
from .user import User
from .product import Product

class UserFavouriteProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)