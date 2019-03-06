from django.db import models


class ShopManager(models.Manager):
    def create_shop(self, name, language, country, currency, image=None):
        """
        Creates and saves a Shop with the given parameters.
        """
        shop = self.model(
            name=name,
            language=language,
            currency=currency,
            shop_profile_image=image
        )
        shop.save(using=self._db)
        return shop
