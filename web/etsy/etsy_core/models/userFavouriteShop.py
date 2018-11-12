from django.db import models
from .user import User
from .shop import Shop

class UserFavouriteShop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)