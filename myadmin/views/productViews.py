
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.urls import reverse
from .. import models
import os,random,time,hashlib

#商品列表显示
def index(request):
    #查询所有会员数据
    data=models.Books.objects.filter().order_by('id')
    # 接收查询条件
    select = request.GET.get('select', None)
    select_text = request.GET.get('select_text', None)
    if select==None:
        if select_text==None:
            data=data.all()
        else:
            data=data.filter(
                Q(bkname__icontains=select_text) |
                Q(bkreco__contains=select_text) |
                Q(bkauthor__contains=select_text) |
                Q(bkbrief__contains=select_text)
            )
    # 实例化分页对象(分页的集合,每页显示多少条数据)
    p = Paginator(data, 7)
    # 接收当前页码数 1为默认值
    index_p = request.GET.get('page', 1)
    # 显示当前页的数据
    newdata = p.page(index_p)
    # 将当前页装入字典返回到网页 将查询条件也存入newdata
    contex = {'data': newdata,'select' : select,'select_text' : select_text}
    return render(request, 'myadmin/product/productindex.html', contex)

#商品添加
def productadd(request):
    if request.method=='GET':
        # 拼接查询所有返回分类列表
        data = models.BookType.objects.extra(
            select={'paths': 'concat(path,id)'}
        ).order_by('paths')
        newdata=showpath(request,data)
        context = {'data_list': newdata}
        return render(request, 'myadmin/product/productAdd.html', context)
    elif request.method=='POST':
        #接收网页的数据
        data=request.POST.dict()
        # 删除token
        data.pop('csrfmiddlewaretoken')
        #接收图书图片
        filelist=request.FILES.getlist('imgurl',None)
        typelsit=request.POST.getlist('bktypeid')
        print(len(typelsit))
        #判断是否有图片
        if len(filelist)<1:
            return HttpResponse(f'<script>alert("请至少选择一张图片");history.back(); </script>')
        elif data['bkname']=='':
            return HttpResponse(f'<script>alert("书名不能为空!");history.back();</script>')
        elif data['bkreco']=='':
            return HttpResponse(f'<script>alert("推荐语不能为空!");history.back(); </script>')
        elif data['bkbrief']=='':
            return HttpResponse(f'<script>alert("简介不能为空!");history.back(); </script>')
        elif data['bkauthor']=='':
            return HttpResponse(f'<script>alert("作者不能为空!");history.back(); </script>')
        elif data['bkpress']=='':
            return HttpResponse(f'<script>alert("出版社不能为空!");history.back(); </script>')
        elif data['bktime']=='':
            return HttpResponse(f'<script>alert("出版时间不能为空!");history.back(); </script>')
        elif data['bkprice']=='':
            return HttpResponse(f'<script>alert("价格不能为空!");history.back(); </script>')
        elif len(typelsit)<1:
            return HttpResponse(f'<script>alert("图书类别不能为空!");history.back();</script>')



        try:
            # 给图书类进行添加
            data.pop('bktypeid')
            obj = models.Books(**data)
            obj.save()
            #判断图书类别是否有多个
            if len(typelsit)>1:
                print('多个种类')
                for id in typelsit:
                    # 将图书类实例对象
                    type_obj = models.BookType.objects.get(id=id)
                    # 图书type类设置关系
                    obj.bktypeid.add(type_obj)
            else:
                # 将图书类实例对象
                type_obj = models.BookType.objects.filter(id=typelsit[0])
                # 图书type类设置关系
                obj.bktypeid.set(type_obj)

            #判断是否为多张图片
            if len(filelist)>1:
                for i in filelist:
                    # 图书的图片处理
                    bkimg = models.BooksImgs()
                    bkimg.imgbkid = obj  # 装对象 因为是外键表
                    bkimg.imgurl = i
                    bkimg.save()
            else:
                # 图书的图片处理
                bkimg = models.BooksImgs()
                bkimg.imgbkid = obj  # 装对象 因为是外键表
                bkimg.imgurl = filelist[0]
                bkimg.save()
            url = reverse('product_index')
            return HttpResponse(f'<script>alert("添加成功");location.href="' + url + '" </script>')
        except:
            url = reverse('product_add')
            return HttpResponse(f'<script>alert("添加失败");location.href="' + url + '" </script>')

#商品删除
def productdelete(request):
    try:
        #接收要删除的ID
        id = request.GET.get('id')
        #因为是图书类 在图库类删除即可
        bkobj=models.Books.objects.get(id=id)
        #这里获取的是这本书所有的图片
        obj=bkobj.booksimgs_set.all()
        #图片删除
        try:
            for i in obj:
                os.remove(f'./{i.imgurl}')
        except:
            return JsonResponse({'code': 2, 'msg': '头像删除失败'})
        obj.delete()

        #清除books类的关系 删除多对多关系表
        bkobj.bktypeid.clear()
        #删除图书表的同时会删除图集表 因为一个图书数据对多个图集数据 1对多
        bkobj.delete()
        return JsonResponse({'code': 0, 'msg': '删除成功'})
    except:
        return JsonResponse({'code': 1, 'msg': '删除失败'})





#商品修改
def productupdate(request):
    if request.method=="GET":
        id=request.GET.get('id')
        obj=models.Books.objects.get(id=id)

        # 拼接查询所有返回分类列表 下拉列表
        data = models.BookType.objects.extra(
            select={'paths': 'concat(path,id)'}
        ).order_by('paths')
        #showpath 增加缩进字符
        newdata = showpath(request, data)
        context={'data':obj,'data_list': newdata}
        return render(request, 'myadmin/product/productupdate.html',context)
    elif request.method=="POST":
        # 接收网页的数据
        data = request.POST.dict()
        # 删除token
        data.pop('csrfmiddlewaretoken')
        #删除编号data自带的 不然无法使用update
        data.pop('id')
        #接收选中的分类列表
        typelsit = request.POST.getlist('bktypeid')
        # 判断条件
        if typelsit:
            print('1')
        elif data['bkname'] == None:
            return HttpResponse(f'<script>alert("书名不能为空!");location.href="history.back();" </script>')
        elif data['bkreco'] == None:
            return HttpResponse(f'<script>alert("推荐语不能为空!");location.href="history.back();" </script>')
        elif data['bkbrief'] == None:
            return HttpResponse(f'<script>alert("简介不能为空!");location.href="history.back();" </script>')
        elif data['bkauthor'] == None:
            return HttpResponse(f'<script>alert("作者不能为空!");location.href="history.back();" </script>')
        elif data['bkpress'] == None:
            return HttpResponse(f'<script>alert("出版社不能为空!");location.href="history.back();" </script>')
        elif data['bktime'] == None:
            return HttpResponse(f'<script>alert("出版时间不能为空!");location.href="history.back();" </script>')
        elif data['bkprice'] == None:
            return HttpResponse(f'<script>alert("价格不能为空!");location.href="history.back();" </script>')
        else:
            return HttpResponse(f'<script>alert("请至少选择一种分类!");location.href="history.back();" </script>')

        # 删除data中的typeid 不然无法使用update
        # data.pop('bktypeid')
        #查询当前要修改的对象
        id=request.POST.get('id')
        obj=models.Books.objects.get(id=id)
        # 图书type类清空关系
        obj.bktypeid.clear()
        obj.bkname = data['bkname']
        obj.bkreco = data['bkreco']
        obj.bkbrief = data['bkbrief']
        obj.bkauthor = data['bkauthor']
        obj.bkpress = data['bkpress']
        obj.bktime = data['bktime']
        obj.bkprice = data['bkprice']
        # 判断图书类别是否有多个
        if len(typelsit) > 1:
            for id in typelsit:
                # 将图书类实例对象
                type_obj = models.BookType.objects.get(id=id)
                # 图书type类设置关系
                obj.bktypeid.add(type_obj)
                obj.save()
        else:
            # 将图书类实例对象
            type_obj = models.BookType.objects.filter(id=typelsit[0])

            # 图书type类设置关系
            obj.bktypeid.set(type_obj)
            obj.save()

        url = reverse('product_index')
        return HttpResponse(f'<script>alert("修改成功");location.href="' + url + '" </script>')




#path换名字显示,缩进 封装函数
def showpath(request,newdata):
    if type(newdata)==models.BookType:
        count = newdata.path.count(',') - 1
        newdata.sj = '>-----' * count
        # 显示父级id名字
        if newdata.fid != 0:
            newdata.fname = models.BookType.objects.get(id=newdata.fid).typename
        # 显示分类路径path
        datanum = list(filter(str.isdigit, newdata.path))
        datalist = ''
        for j in datanum:
            if j == '0':
                datalist += '顶级分类,'
            else:
                typename = models.BookType.objects.get(id=j).typename
                datalist += typename + ','
        newdata.datalist = datalist
    else:
        for i in newdata:
            count = i.path.count(',') - 1
            i.sj = '>-----' * count
            # 显示父级id名字
            if i.fid != 0:
                i.fname = models.BookType.objects.get(id=i.fid).typename
            # 显示分类路径path
            # datanum = list(filter(str.isdigit, i.path))
            datanum=list(str(i.path).split(','))#path装进列表 用split分割
            del(datanum[-1])#将列表最后一个数据删除 因为是,'' 是空的
            datalist = ''
            for j in datanum:
                if j == '0':
                    datalist += '顶级分类,'
                else:
                    typename = models.BookType.objects.get(id=j).typename
                    datalist += typename + ','
            i.datalist = datalist
    return newdata