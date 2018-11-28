from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .userManager import UserManager
from PIL import Image
from .shoppingCart import ShoppingCart


import os


def get_image_path(instance, filename):
    return os.path.join('user', str(instance.id), filename)


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    
    favourite_shops = models.ManyToManyField('Shop', through='UserFavouriteShop')
    favourite_products = models.ManyToManyField('Product', through='UserFavouriteProduct')
    # notice the absence of a "Password field", that's built in.

    # Our own properties
    has_shop = models.BooleanField(default=False)
    first_name = models.CharField(
        verbose_name='user first name',
        max_length=45,
        null=True,)
    last_name = models.CharField(
        verbose_name='user last name',
        max_length=45,
        null=True)
    profile_image = models.ImageField(
        upload_to=get_image_path, blank=True, null=True)
    cart = models.ForeignKey(
        ShoppingCart, on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'email'
    # Email & Password are required by default.
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        # The user is identified by their name
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        # The user is identified by their fisrt name
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return self.email

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

    @property
    def is_has_shop(self):
        "Does the user has a shop?"
        return self.has_shop

    objects = UserManager()
