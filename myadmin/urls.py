
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    #后台管理主页
    path('',indexViews.index,name='home_index'),
    path('login',indexViews.login,name='home_login'),
    path('yzm',indexViews.verifycode,name='home_yzm'),
    path('exit',indexViews.exit,name='home_exit'),

    #后台用户管理
    path('meber/index',meberViews.index,name='meber_index'),
    path('meber/meberadd',meberViews.meberadd,name='meber_add'),
    path('meber/meberup',meberViews.meberupdate,name='meber_update'),
    path('meber/meberdel',meberViews.meberdelete,name='meber_delete'),
    #后台分类管理
    path('type/index',typeViews.index,name='type_index'),
    path('type/typeadd',typeViews.typeadd,name='type_add'),
    path('type/typeup',typeViews.typeupdate,name='type_update'),
    path('type/typedel',typeViews.typedelete,name='type_delete'),
    #后台图书管理
    path('product/index',productViews.index,name='product_index'),
    path('product/productadd',productViews.productadd,name='product_add'),
    path('product/productup',productViews.productupdate,name='product_update'),
    path('product/productdel',productViews.productdelete,name='product_delete'),
    #后台订单管理
    path('order/index',orderViews.index,name='order_index'),


]
