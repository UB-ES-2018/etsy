from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.sign_up, name='signup'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^shop/$', views.create_shop, name='create_shop'),
    url(r'^shop/(?P<shop_id>.*)/', views.shop, name='shop'),
    url(r'^shop/(?P<shop_id>.*)/product/$', views.products, name='products')
]
