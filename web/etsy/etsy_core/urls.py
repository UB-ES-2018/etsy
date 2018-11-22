from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # Auth
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # Shop
    path('shop/', views.create_shop, name='create_shop'),
    path('shop/<int:shop_id>/', views.shop, name='shop'),
    path('shop/<int:shop_id>/logo', views.shop_logo, name='shop_logo'),
    path('shop/<int:shop_id>/userfavshop',
         views.update_user_favourite_shop, name='update_user_favourite_shop'),
    # Products
    path('shop/<int:shop_id>/product/',
         views.create_product, name='create_product'),
    path('shop/<int:shop_id>/product/<int:product_id>/',
         views.product, name='product'),
    path('product/<int:product_id>/image',
         views.product_image, name='product_image'),
    # Profile
    path('profile/<int:user_id>/', views.profile, name="profile"),
    path('profile/<int:user_id>/avatar', views.user_avatar, name="user_avatar"),
    # Search
    path('search/', views.search_results, name="search"),
    # Cart
    path('cart/', views.shopping_cart, name="cart"),
    path('cart/<action>/<int:product_id>',
         views.cart_action, name="cart_action"),
    # Checkout
    path('checkout/', views.checkout, name='checkout'),
]
