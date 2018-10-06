from django.db import models


class Shop(models.Model):
    name = models.CharField(
        verbose_name='shop_name',
        max_length=20,
        null=True,)
    language = models.CharField(
        verbose_name='shop_language',
        max_length=20,
        null=True,)
    currency = models.CharField(
        verbose_name='shop_currency',
        max_length=45,
        null=True,)

    has_items = models.BooleanField(default=False)

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
        "Is the user active?"
        return self.has_items
