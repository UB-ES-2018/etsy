from django.db import models


class ProductManager(models.Manager):
    def create_product(self, name, shop_id, description, price):
        """
        Creates and saves a product with the given parameters.
        """
        product = self.model(
            name=name,
            shop_id=shop_id,
            description=description,
            price=price
        )
        product.save(using=self._db)
        return product
