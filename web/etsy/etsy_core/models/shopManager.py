from django.db import models


class ShopManager(models.Manager):
    def create_shop(self, name, language, country, currency, has_items=False, image = None):
        """
        Creates and saves a Shop with the given parameters.
        """
        if not name:
            raise ValueError('Shops must have a name.')

        if not language:
            raise ValueError('Shops must have a defined language.')

        if not currency:
            raise ValueError('Shops must have a defined currency.')

        if not country:
            raise ValueError('Shops must have a defined country.')

        shop = self.model(
            name=name,
            language=language,
            currency=currency,
            has_items=has_items,
            shop_profile_image=image
        )
        shop.save(using=self._db)
        return shop
