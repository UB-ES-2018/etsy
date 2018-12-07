from django.db import models
from .product import Product
from .user import User

class ProductReview(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=False)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"ID: {self.id} - (PRODUCT: {self.product} - USER: {self.user} - RATING: {self.rating})"