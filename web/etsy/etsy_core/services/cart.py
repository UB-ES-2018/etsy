from ..models import ShoppingCart, ProductOnCart


class CartHandler:
    @staticmethod
    def get_cart(user):
        if not user.cart:
            user.cart = ShoppingCart.objects.create()
            user.save()

        return user.cart

    @staticmethod
    def add_product_to_cart(user, product):
        cart = CartHandler.get_cart(user)
        try:
            prod = ProductOnCart.objects.get(cart=cart, product=product)
            prod.amount += 1
            prod.save()
        except:
            ProductOnCart.objects.create(cart=cart, product=product, amount=1)
        return cart

    @staticmethod
    def get_items_of_cart(user):
        cart = CartHandler.get_cart(user)
        return cart.productoncart_set.all()