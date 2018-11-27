from ..models import ShoppingCart, ProductOnCart
from django.http import Http404

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
    def remove_product_from_cart(user, product):
        cart = CartHandler.get_cart(user)
        try:
            prod = ProductOnCart.objects.get(cart=cart, product=product)
            prod.delete()
        except:
            raise Http404("Product does not exist")
        return cart

    @staticmethod
    def get_items_of_cart(user):
        cart = CartHandler.get_cart(user)
        return cart.items.all()

    @staticmethod
    def get_total(user):
        cart = CartHandler.get_cart(user)
        total_amount = 0
        
        for item in cart.items.all():
            total_amount += (item.product.price * item.amount)

        return total_amount
    
    @staticmethod
    def set_amount(user, product, qty):
        cart = CartHandler.get_cart(user)
        try:
            prod = ProductOnCart.objects.get(cart=cart, product=product)
            prod.amount = qty
            prod.save()
            if qty == 0:
                CartHandler.remove_product_from_cart(user, prod)
        except:
            raise Http404("Product does not exist")
        return cart