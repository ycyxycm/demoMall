import random
from django.contrib.sites import requests
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.urls import reverse
from myadmin import models
from django.contrib.auth.hashers import make_password, check_password


#购物车页面
def index(request):
    #接收当前用户
    myuser=request.session.get('myuser')
    #查询当前用户所有购物车信息
    data=models.ShoppingCart.objects.filter(uid=myuser['id'])
    #装入集合
    context={'data':data}
    return render(request,'mybook/cart.html',context)

#购物车添加
def addcart(request):
    #接收post请求及数据
    data=request.POST.dict()
    # 删除token
    data.pop('csrfmiddlewaretoken')
    #接收当前用户
    myuser=request.session.get('myuser')

    #验证用户是否登录
    if not myuser['id']:
        return JsonResponse({'code':1,'msg':'当前用户没有登录'})

    #将data中的id转为对象
    data['bid']=models.Books.objects.get(id=data['bid'])
    data['uid']=models.Users.objects.get(id=myuser['id'])
    try:
        # 判断购物车里是否已经有了这个商品
        zzobj = models.ShoppingCart.objects.filter(bid=data['bid']).count()
        if zzobj:
            return JsonResponse({'code': 3, 'msg': '购物车里已经有此图书,去购物车增加数量即可!'})
        #进行数据库操作
        cartobj=models.ShoppingCart(**data)
        cartobj.save()
        return JsonResponse({'code':0,'msg':'加入购物车成功'})
    except:
        return JsonResponse({'code': 2, 'msg': '加入购物车失败'})

#购物车删除
def delcart(request):
    # 接收购物车信息id
    cartid = request.GET.get('cartid')

    try:
        obj = models.ShoppingCart.objects.get(id=cartid)
        obj.delete()
        return JsonResponse({'code': 0,'msg':'删除成功!'})
    except:
        return JsonResponse({'code': 1,'msg':'删除失败!'})

#是否选中按钮修改
def upchecked(request):
    # 接收购物车信息id
    cartid = request.GET.get('cartid',None)
    # 接收要修改的是否选中
    select = request.GET.get('select')
    try:
        if cartid == None:
            data=models.ShoppingCart.objects.filter().update(select=select)
        else:
            obj=models.ShoppingCart.objects.get(id=cartid)
            obj.select=select
            obj.save()
        return JsonResponse({'code': 0, 'msg': '修改按钮成功'})
    except:
        return JsonResponse({'code': 1, 'msg': '修改按钮失败'})


#购物车信息修改
def upcart(request):
    #接收购物车信息id
    cartid=request.GET.get('cartid')
    #接收要修改的数量
    number=request.GET.get('number')
    try:
        obj=models.ShoppingCart.objects.get(id=cartid)
        obj.number=number
        obj.save()
        return JsonResponse({'code':0,'msg': '修改数量成功'})
    except:
        return JsonResponse({'code': 1,'msg': '修改数量失败'})