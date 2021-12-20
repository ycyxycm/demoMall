import os

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.urls import reverse
from .. import models

#分类列表显示
def index(request):
    #拼接查询
    data=models.BookType.objects.extra(
        select={'paths':'concat(path,id)'}
    ).order_by('paths')

    # 接收查询条件
    select = request.GET.get('select', None)
    select_text = request.GET.get('select_text', None)
    # 判断是否有查询条件
    if select:
        if select == 'select_all':
            data = data.all()
        elif select == 'select_fid':
            data = data.filter(fid=select_text)
    #查询所有返回select列表
    data_list=models.BookType.objects.all()

    # 实例化分页对象(分页的集合,每页显示多少条数据)
    p = Paginator(data, 7)
    # 接收当前页码数 1为默认值
    index_p = request.GET.get('page', 1)
    # 显示当前页的数据
    newdata = p.page(index_p)
    #添加分类缩进 显示父级id名字
    newdata=showpath(request,newdata)
    context={'data':newdata,'select_text':select_text,'data_list':data_list}
    return render(request,'myadmin/type/typeindex.html',context)


#分类添加
def typeadd(request):
    if request.method=='GET':
        data=models.BookType.objects.all()
        context={'data':data}
        return render(request,'myadmin/type/typeAdd.html',context)
    elif request.method=='POST':
        #将网页post请求数据装进字典
        data=request.POST.dict()
        # 删除token
        data.pop('csrfmiddlewaretoken')
        #添加顶级分类
        if data['fid']=='0':
            data['path']='0,'
        else:
            #查询父类的path加入到自己的path
            obj=models.BookType.objects.get(id=data['fid'])
            data['path']=obj.path+data['fid']+','
        try:
            obj=models.BookType(**data)
            obj.save()

            url = reverse('type_index')
            return HttpResponse(f'<script>alert("添加成功");location.href="' + url + '" </script>')
        except:
            url = reverse('type_add')
            return HttpResponse(f'<script>alert("添加失败");location.href="' + url + '" </script>')

#分类删除
def typedelete(request):
    try:
        #先删除自己这个类 假如有子类将全部删除
        id = request.GET.get('id')
        obj = models.BookType.objects.get(id=id)
        deleteson(request,obj)
        #删除
        obj.delete()
        return JsonResponse({'code': 0, 'msg': '删除成功'})
    except:
        return JsonResponse({'code': 1, 'msg': '删除失败'})


#分类修改
def typeupdate(request):
    if request.method=='GET':
        id = request.GET.get('id')
        obj = models.BookType.objects.get(id=id)
        obj_all=models.BookType.objects.all()
        newdata=showpath(request,obj)
        context={'data':newdata,'data_all':obj_all}
        return render(request,'myadmin/type/typeUpdate.html',context)

    elif request.method=='POST':
        try:
            # 将网页post请求数据装进字典
            data = request.POST.dict()
            # 删除token
            data.pop('csrfmiddlewaretoken')
            #需要修改的对象
            obj=models.BookType.objects.get(id=data['id'])
            #改变父id
            obj.fid=data['fid']
            #改变path
            newobj=models.BookType.objects.get(id=data['fid'])
            obj.path=f'{newobj.path}{newobj.id},'
            obj.typename=data['typename']
            obj.save()
            url = reverse('type_index')
            return HttpResponse(f'<script>alert("修改成功");location.href="' + url + '" </script>')
        except:
            url = reverse('type_update')
            return HttpResponse(f'<script>alert("修改失败");location.href="' + url + '" </script>')



#删除操作删除子类和子子类 删除儿孙两代
def deleteson(request,obj):
    print('进入删除子类方法')
    data = models.BookType.objects.filter(fid=obj.id)
    for i in data:
        if i == None:
            print('没有子类')
        else:  # 有的话
            # #删除子子类
            # sonsondata=models.BookType.objects.filter(fid=i.id)
            # for x in sonsondata:
            #     if x == None:
            #         print("没有子子类")
            #     else:#有的话
            #         #删除子子类
            #         x.delete()
            deleteson(request,i)

            # 删除子类
            i.delete()




#path换名字显示,缩进 封装函数
def showpath(request,newdata):
    print(type(newdata))
    if type(newdata)==models.BookType:
        count = newdata.path.count(',') - 1
        newdata.sj = '>-----' * count
        # 显示父级id名字
        if newdata.fid != 0:
            newdata.fname = models.BookType.objects.get(id=newdata.fid).typename
        # 显示分类路径path
        # datanum = list(filter(str.isdigit, newdata.path))
        datanum = list(str(newdata.path).split(','))  # path装进列表 用split分割
        del (datanum[-1])  # 将列表最后一个数据删除 因为是,'' 是空的
        datalist = ''
        for j in datanum:
            if j == '0':
                datalist += '顶级分类,'
            else:
                typename = models.BookType.objects.get(id=j).typename
                datalist += typename+ ','
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

