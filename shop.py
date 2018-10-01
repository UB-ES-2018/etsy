rom django.db import models


class Shop():
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
    has_item = model.BooleanField(default=False)

    # Our own properties

    USERNAME_FIELD = 'name'
    # Email & Password are required by default.
    REQUIRED_FIELDS = ['name', 'language', 'currency']

    def get__name(self):
        # The shop is identified by its name
        return self.name

    def get_language(self):
        # The shop has a default language defined by the owner
        return self.language

    def get_currency(self):
        #The shop owner works with a currency
        return self.currency

    def is_has_item(self):
        return self.has_item
   # def __str__(self):              # __unicode__ on Python 2
    #    return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active



