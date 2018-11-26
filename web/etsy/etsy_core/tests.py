from django.test import TestCase
from .models import User, Shop, UserFavouriteShop, Product, UserFavouriteProduct, Categories
from .forms import ShopForm, RegisterForm, LoginForm, ProductForm
from django.test import Client
# Create your tests here.


class UserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com', first_name="Joe", last_name="Doe")

    def test_get_user_full_name(self):
        self.assertEqual(self.user.get_full_name(), "Joe Doe")

    def test_get_user_first_name(self):
        self.assertEqual(self.user.get_short_name(), "Joe")

    def test_get_user_permisions(self):
        self.assertTrue(self.user.has_perm('perm'))

    def test_default_user_is_not_staff(self):
        self.assertFalse(self.user.is_staff)

    def test_default_user_is_not_admin(self):
        self.assertFalse(self.user.is_admin)

    def test_user_with_a_shop_has_shop(self):
        form = ShopForm({
            'name': "Premium Linen",
            'language': "1",
            'country': "1",
            'currency': "2"
        }, user=self.user)
        form.save()
        self.assertTrue(self.user.has_shop)

    def test_user_favourite_shop(self):
        shop = Shop()
        shop.save()
        UserFavouriteShop.objects.create(user=self.user, shop=shop)
        self.assertEqual(self.user.favourite_shops.all()[0], shop)

    def test_user_favourite_product(self):
        shop = Shop(shop_owner=self.user)
        shop.save()
        category = Categories.objects.create(category_name='cn')
        product = Product.objects.create(shop_id=shop, price=0.1, categories=category)  

        UserFavouriteProduct.objects.create(user=self.user, product=product)
        self.assertEqual(self.user.favourite_products.all()[0],product)

        UserFavouriteProduct.objects.filter(user=self.user, product=product).delete()
        self.assertTrue(len(self.user.favourite_products.all())==0 )


class ShopTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com', first_name="Joe", last_name="Doe")

    def test_valid_data(self):
        form = ShopForm({
            'name': "Premium Linen",
            'language': "1",
            'country': "1",
            'currency': "2"
        }, user=self.user)

        self.assertTrue(form.is_valid())
        shop = form.save()

        self.assertEqual(shop.name, "Premium Linen")
        self.assertEqual(shop.language, "1")
        self.assertEqual(shop.country, "1")

    def test_blank_data(self):
        form = ShopForm({}, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['This field is required.'],
            'language': ['This field is required.'],
            'country': ['This field is required.'],
            'currency': ['This field is required.'],
        })

    def test_linking_user(self):
        form = ShopForm({
            'name': "Premium Linen",
            'language': "1",
            'country': "1",
            'currency': "2"
        }, user=self.user)

        shop = form.save()
        self.assertEqual(self.user.shop, shop)
        self.assertEqual(shop.shop_owner, self.user)


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com', first_name="Joe", last_name="Doe", password="testpassword")

    def test_sign_up_form(self):
        form = RegisterForm({
            'email': "joe.doe@test.com",
            'first_name': "Joe",
            'last_name': "Doe",
            'password1': "testpassword",
            "password2": "testpassword"
        })

        self.assertTrue(form.is_valid())
        user = form.save()

        self.assertEqual(user.first_name, "Joe")

    def test_login_form(self):
        form = LoginForm({
            'email': "user@test.com",
            'password': "testpassword"
        })

        print(form.errors)
        self.assertTrue(form.is_valid())

        c = Client()
        self.assertTrue(
            c.login(email="user@test.com", password="testpassword"))

    def test_login_fails_with_wrong_email(self):
        c = Client()
        self.assertFalse(
            c.login(email="user_not@test.com", password="testpassword"))

    def test_login_fails_with_wrong_password(self):
        c = Client()
        self.assertFalse(
            c.login(email="user@test.com", password="1234"))
