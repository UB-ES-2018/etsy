from django.test import TestCase
from .models import User, Shop, UserFavouriteShop, Product, UserFavouriteProduct, Categories
from .forms import ShopForm, RegisterForm, LoginForm, ProductForm
from .services import CartHandler
from django.test import Client
from decimal import Decimal
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

class ProductTests(TestCase):
    def setUp(self):
        self.shop = Shop(name="Random shop",language='1',country='1',currency='1')
        self.cat = Categories(category_name="asd", is_default=True)
        self.cat.save()
        self.shop.save()

    def test_valid_data(self):
        form = ProductForm({
            'name': "Wood table",
            'description': "A table made of wood",
            'tags': "table",
            'categories': self.cat.id,
            'price': 9.99
        }, shop_id = self.shop.id)
        self.assertEquals(form.errors, {})
        self.assertTrue(form.is_valid())
        
        product = form.save()

        self.assertEqual(product.name, "Wood table")
        self.assertEqual(product.price, Decimal('9.99'))
        self.assertEqual(product.description, "A table made of wood")
        self.assertEqual(product.shop_id.id, self.shop.id)

    def test_blank_data(self):
        form = ProductForm({}, shop_id=self.shop.id)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors,{
            'name': ['This field is required.'],
            'description': ['This field is required.'],
            'tags': ['This field is required.'],
            'price': ['This field is required.'],
            'categories': ['This field is required.'],
        })

    def test_user_favourite_product(self):
        pass
        '''
        shop = Shop(shop_owner=self.user)
        shop.save()
        category = Categories.objects.create(category_name='cn')
        product = Product.objects.create(shop_id=shop, price=0.1, categories=category)  

        UserFavouriteProduct.objects.create(user=self.user, product=product)
        self.assertEqual(self.user.favourite_products.all()[0],product)

        UserFavouriteProduct.objects.filter(user=self.user, product=product).delete()
        self.assertTrue(len(self.user.favourite_products.all())==0 )
        '''

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

    def test_repeated_shop_name(self):
        form = ShopForm({
            'name': "Premium Linen",
            'language': "1",
            'country': "1",
            'currency': "2"
        }, user=self.user)

        self.assertTrue(form.is_valid())
        shop = form.save()

        form = ShopForm({
            'name': "Premium Linen",
            'language': "1",
            'country': "1",
            'currency': "2"
        }, user=self.user)

        self.assertFalse(form.is_valid())
        
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

class ManagerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com', first_name="Joe", last_name="Doe", password="testpassword")

    def test_create_product_manager(self):
        shop = Shop()
        shop.save()
        product = Product.objects.create_product("Test", shop, "test", 9.99)
        self.assertEqual(product.name, "Test")

    def test_create_shop_manager(self):
        shop = Shop.objects.create_shop("Shop", "EN", "Spain", "GBP", image = None)
        self.assertEqual(shop.name, "Shop")

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


class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com', first_name="Joe", last_name="Doe", password="testpassword")

    def test_index_renders(self):
        response = self.client.get('/', follow=True)
        self.assertTemplateUsed(response, 'home.html')

    def test_login_post_works(self):
        response = self.client.post('/login/', {'email': 'user@test.com', 'password': 'testpassword'})
        self.assertRedirects(response ,'/')

    def test_logout(self):
        response = self.client.get('/logout/')
        self.assertRedirects(response ,'/')

    def test_checkout_renders(self):
        self.client.login(email="user@test.com", password="testpassword")  # defined in fixture or with factory in setUp()
        response = self.client.get('/checkout/')
        self.assertTemplateUsed(response ,'confirmation_view.html')

    def test_signup_renders(self):
        response = self.client.get('/signup/', follow=True)
        self.assertTemplateUsed(response, 'signup.html')

    def test_payment_renders(self):
        response = self.client.get('/payment/', follow=True)
        self.assertTemplateUsed(response, 'payment_view.html')

    def test_signup_post_works(self):
        response = self.client.post('/signup/', {'email':'user2@test.com', 'first_name':"Joe2", 'last_name':"Doe2", 'password1':"testpassword2", 'password2':"testpassword2"})
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_signup_redirets_if_user_auth(self):
        self.client.login(email="user@test.com", password="testpassword")  # defined in fixture or with factory in setUp()
        response = self.client.get('/signup/')
        self.assertRedirects(response, '/')

    def test_call_shop_denies_anonymous(self):
        response = self.client.get('/shop/', follow=True)
        self.assertRedirects(response, '/login/?next=/shop/')
        response = self.client.post('/shop/', follow=True)
        self.assertRedirects(response, '/login/?next=/shop/')

    def test_call_view_loads(self):
        self.client.login(email="user@test.com", password="testpassword")  # defined in fixture or with factory in setUp()
        response = self.client.get('/shop/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop_creation.html')

class TestServices(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com', first_name="Joe", last_name="Doe", password="testpassword")
        form = ShopForm({
            'name': "Premium Linen",
            'language': "1",
            'country': "1",
            'currency': "2"
        }, user=self.user)
        self.shop = form.save()
        self.product = Product.objects.create_product("Test", self.shop, "test", 10.0)

    def test_add_product(self):
        CartHandler.add_product_to_cart(self.user, self.product)
        self.assertTrue(len(CartHandler.get_items_of_cart(self.user)))

    def test_add_two_same_product(self):
        CartHandler.add_product_to_cart(self.user, self.product)
        CartHandler.add_product_to_cart(self.user, self.product)
        self.assertEquals(CartHandler.get_items_of_cart(self.user)[0].amount,2)

    def test_remove_product_cart(self):
        CartHandler.add_product_to_cart(self.user, self.product)
        CartHandler.remove_product_from_cart(self.user, self.product)
        self.assertFalse(len(CartHandler.get_items_of_cart(self.user)))

    def test_empty_cart(self):
        CartHandler.add_product_to_cart(self.user, self.product)
        CartHandler.add_product_to_cart(self.user, self.product)
        CartHandler.empty_cart(self.user)
        self.assertFalse(len(CartHandler.get_items_of_cart(self.user)))

    def test_total_cart(self):
        CartHandler.add_product_to_cart(self.user, self.product)
        CartHandler.add_product_to_cart(self.user, self.product)
        total = CartHandler.get_total(self.user)
        self.assertEquals(total, Decimal(20.0))

    def test_set_amount(self):
        CartHandler.add_product_to_cart(self.user, self.product)
        CartHandler.set_amount(self.user, self.product, 10)
        self.assertEquals(CartHandler.get_items_of_cart(self.user)[0].amount,10)