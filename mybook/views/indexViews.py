import random
from django.contrib.sites import requests
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.urls import reverse
from myadmin import models
from django.contrib.auth.hashers import make_password, check_password

#前台页面跳转
def index(request):
    #左边列表显示
    data=models.BookType.objects.filter(fid=0)
    #添加一个子类图书集合data_son
    for i in data:
        print(i.typename)
        data_son=models.BookType.objects.filter(path__icontains=i.id)
        i.data_son=data_son

    #装入集合
    context={'data':data}
    return render(request, 'mybook/index.html',context)

#商品列表显示
def list(request):
    #下拉列表显示
    data = models.BookType.objects.filter(fid=0)
    #获取图书类别id
    typeid=request.GET.get('typeid')
    #获取查询条件post表单
    textselect=request.GET.get('text_select')
    #判断是否有查询条件
    if textselect!=None:
        data_select=models.Books.objects.filter(bkname__icontains=textselect)
    else:
        data_select=models.Books.objects.filter()
    #查询
    if typeid==None:#没有图书类别
        bkdata=data_select.all().order_by('id')
        pathlist=''
        newbk = models.Books.objects.filter().last()
    else:#有图书类别
        obj=models.BookType.objects.get(id=typeid)
        # 新书推荐
        newbk = models.Books.objects.filter(bktypeid=obj).last()
        #对path进行解释
        list=obj.path[:-1]
        list=list.split(',')
        del list[0]  #删除path第一个0
        list.append(str(obj.id))
        pathlist=[]
        for x in list:
            pathlist.append(models.BookType.objects.get(id=x))
        #通过图书类别查出来的book
        bkdata=data_select.filter(bktypeid=obj).order_by('id')
    # 实例化分页对象(分页的集合,每页显示多少条数据)
    p = Paginator(bkdata, 15)
    # 接收当前页码数 1为默认值
    index_p = request.GET.get('page', 1)
    # 显示当前页的数据
    bkdata = p.page(index_p)
    #装入集合
    context={'data':data,'bkdata':bkdata,'path':pathlist,'text_select':textselect,'newbk':newbk}
    return render(request,'mybook/list.html',context)


#商品详细信息显示
def info(reuqest):
    # 下拉列表显示
    data = models.BookType.objects.filter(fid=0)
    #接收图书id
    id=reuqest.GET.get('id')
    #查询图书信息
    obj=models.Books.objects.get(id=id)
    #新品推荐
    newbk=models.Books.objects.all().order_by('-id')[:2] #逆序排序取头两个数据返回


    #返回字典
    context={'data':data,'obj':obj,'newbk':newbk}
    return render(reuqest,'mybook/info.html',context)
