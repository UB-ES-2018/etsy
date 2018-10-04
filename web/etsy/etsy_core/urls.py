from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'^shop/$', views.create_shop, name='shop'),
    path(r'^shop/(?P<shop_id>.*)/', views.shop, name='shop'),
    path(r'^shop/(?P<shop_id>.*)/product/$', views.create_product, name='shop'),
    path(r'^shop/(?P<shop_id>.*)/product/(?P<product_id>.*)/', views.product, name='shop')
]
