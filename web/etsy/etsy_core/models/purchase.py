from django.db import models

from .product import Product
from .user import User

class Purchase(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="purchases", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
    sell_price = models.DecimalField(max_digits=8, decimal_places=2)
    reviewed = models.BooleanField(default=False)
    purchase_date = models.DateField(auto_now_add=True)