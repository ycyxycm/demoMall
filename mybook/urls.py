
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    #用户登录 注册 退出

    #用户登录
    path('login',userViews.userlogin,name='mybook_login'),
    #用户注册
    path('register',userViews.userregister,name='mybook_register'),
    #用户推出
    path('exit',userViews.userexit,name='mybook_exit'),
    #ajax验证手机号码是否存在
    path('ckphone',userViews.checkphone,name='mybook_ckphone'),
    #手机短信验证码按钮
    path('sendcoke',userViews.sendcoke,name='mybook_sendcoke'),
    #用户中心----个人信息
    path('usercenterinfo',userViews.usercenterinfo,name='mybook_usercenterinfo'),

    #主页面显示
    #商城主页面
    path('',indexViews.index,name='mybook_index'),
    #商城商品列表显示
    path('list',indexViews.list,name='mybook_list'),
    #商城商品详细信息
    path('info',indexViews.info,name='mybook_info'),

    #购物车页面
    path('shoppingcart',cartViews.index,name='mybook_cart'),
    #购物车添加商品
    path('shoppingcartadd',cartViews.addcart,name='mybook_addcart'),
    #购物车删除商品
    path('shoppingcartdel',cartViews.delcart,name='mybook_delcart'),
    #购物车修改商品
    path('shoppingcartup',cartViews.upcart,name='mybook_upcart'),
    #购物车修改选择按钮
    path('shoppingcartcheckedup',cartViews.upchecked,name='mybook_upchecked'),

    #订单
    #提交订单
    path('submitorder',userorderViews.submitorder,name='mybook_suborder'),
    #订单列表页面 支付成功跳转的地址
    path('orderlist',userorderViews.orderlist,name='mybook_orderlist'),

    #收货地址页面
    path('receivingaddress',userViews.receaddress,name='mybook_receaddress'),
    #修改收货地址默认项
    path('upreceselect',userViews.upreceselect,name='mybook_upreceselect'),

    # 支付宝回调地址
    path('pay_result',userorderViews.pay_result,name='mybook_pay_result'),
]
