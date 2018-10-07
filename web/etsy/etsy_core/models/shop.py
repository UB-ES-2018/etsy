from django.db import models
from .user import User

from .shopManager import ShopManager


class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name='shop_name',
        max_length=20,
        null=True,)
    language = models.CharField(
        verbose_name='shop_language',
        max_length=20,
        null=True,)
    country = models.CharField(
        verbose_name='shop_country',
        max_length=20,
        null=True, )
    currency = models.CharField(
        verbose_name='shop_currency',
        max_length=45,
        null=True,)

    has_items = models.BooleanField(default=False)
    shop_owner = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    # Our own properties

    def get__name(self):
        # The shop is identified by its name
        return self.name

    def get_language(self):
        # The shop has a default language defined by the owner
        return self.language

    def get_currency(self):
        # The shop owner works with a currency
        return self.currency

    @property
    def has_items(self):
        "The shop offer some item?"
        return self.has_items

    objects = ShopManager()
