from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.sign_up, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('shop/', views.create_shop, name='create_shop'),
    path('shop/<int:shop_id>/', views.shop, name='shop'),
    path('shop/<int:shop_id>/product/',
         views.create_product, name='create_product'),
    path('shop/<int:shop_id>/product/<int:product_id>/',
         views.product, name='product'),
    path('profile/<int:user_id>/', views.profile, name = "profile")
]
