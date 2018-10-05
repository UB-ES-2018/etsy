from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^signup/$', views.sign_up, name='signup'),
    path(r'^shop/$', views.create_shop, name='shop'),
    path(r'^shop/(?P<shop_id>.*)/', views.shop, name='shop'),
]
