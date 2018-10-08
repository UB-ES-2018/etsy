from django.db import models


class ProductManager(models.Manager):
    def create_product(self, name, shop_id):
        """
        Creates and saves a product with the given parameters.
        """
        if not name:
            raise ValueError('Products must have a name.')

        if not shop_id:
            raise ValueError('Products must belong to a shop.')

        product = self.model(
            name=name,
            shop_id=shop_id
        )
        product.save(using=self._db)
        return product
