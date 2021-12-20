import os,random,time,hashlib
from django.http import JsonResponse
from .. import models
from django.shortcuts import render,HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password


#列表显示
def index(request):
    # 查询所有会员数据
    data = models.Users.objects.filter()

    #接收查询条件
    select = request.GET.get('select',None)
    select_text=request.GET.get('select_text',None)
    # 判断是否有查询条件
    if select:
        if select=='select_all':
            data=data.all()
        elif select == 'select_nikename':
            data=data.filter(nikename__icontains=select_text)
        elif select == 'select_sex':
            if select_text=='女':
                data = data.filter(sex__icontains=0)
            elif select_text=='男':
                data = data.filter(sex__icontains=1)
        elif select == 'select_phone':
            data=data.filter(phone__icontains=select_text)
        elif select == 'select_address':
            data=data.filter(homeaddress__icontains=select_text)
        elif select == 'select_usertype':
            data=data.filter(usertype__icontains=select_text)

    #实例化分页对象(分页的集合,每页显示多少条数据)
    p=Paginator(data,5)
    #接收当前页码数 1为默认值
    index_p=request.GET.get('page',1)
    #显示当前页的数据
    newdata=p.page(index_p)
    #将当前页装入字典返回到网页 将查询条件也存入newdata
    contex={'data':newdata,'select':select,'select_text':select_text}
    return render(request,'myadmin/meber/meberindex.html',contex)

#会员注册
def meberadd(request):
    if request.method=='GET':
        return render(request, 'myadmin/meber/meberAdd.html')
    else:
        try:
            # 接收表单数据
            data = request.POST.dict()
            #删除token
            data.pop('csrfmiddlewaretoken')
            #密码加密
            # data['password']=password_md5(data['password'])
            data['password'] = make_password(data['password'])
            #接收图片
            file=request.FILES.get('face',None)
            if file:
                # 将图片路径保存
                filename = img_upload(file)
                # 存进字典
                data['face'] = filename
            else:
                # #没有上传头像则设置默认头像
                # data['face']='/static/myadmin/images/face/default_face.jpg'
                data.pop('face')
            #验证手机号码是否存在
            # 验证
            obj = models.Users.objects.filter(phone=data['phone']).count()
            # 判断
            if obj:
                url = reverse('meber_add')
                return HttpResponse(f'<script>alert("手机号码已注册!");location.href="' + url + '" </script>')
            # 存进数据库
            obj = models.Users(**data)
            # 数据库提交
            obj.save()
            url=reverse('meber_index')
            return HttpResponse(f'<script>alert("注册成功");location.href="' + url + '" </script>')
        except:
            url=reverse('meber_add')
            return HttpResponse(f'<script>alert("注册失败");location.href="' + url + '" </script>')

#会员修改
def meberupdate(request):
    if request.method=='GET':
        id=request.GET.get('id')
        obj=models.Users.objects.get(id=id)
        conte={'obj':obj}
        return render(request,'myadmin/meber/meberUpdate.html',conte)
    elif request.method=="POST":
        # 接收表单数据
        data = request.POST.dict()
        # 删除token
        data.pop('csrfmiddlewaretoken')
        # 密码加密
        data['password'] = make_password(data['password'])
        # 接收图片
        file = request.FILES.get('face', None)
        if file:
            # 将图片路径保存
            filename = img_upload(file)
            # 存进字典
            data['face'] = filename
        else:
            data.pop('face')
        #数据库进行更新
        try:
            obj=models.Users.objects.filter(id=data['id'])
            obj.update(**data)
            url = reverse('meber_index')
            return HttpResponse(f'<script>alert("修改成功");location.href="' + url + '" </script>')
        except:
            url =reverse('meber_update')
            urlname=f"{url}+?id={{ i.id }}"
            return HttpResponse(f'<script>alert("修改失败");location.href="' + urlname + '" </script>')


#会员删除
def meberdelete(request):
    try:
        id=request.GET.get('id')
        obj=models.Users.objects.get(id=id)
        try:
            if obj.face!='/static/myadmin/images/face/default_face.jpg':
                os.remove('.'+obj.face)
        except:
            return JsonResponse({'code': 2, 'msg': '头像删除失败'})
        obj.delete()
        return JsonResponse({'code': 0, 'msg': '删除成功'})
    except:
        return JsonResponse({'code': 1, 'msg': '删除失败'})
#封装MD5加密
def password_md5(msg):
    hl = hashlib.md5()
    hl.update(msg.encode(encoding='utf-8'))
    return hl.hexdigest()
#封装图片上传到服务器
def img_upload(file):

    if file:  # 假如file有数据的话则
        # 处理上传文件
        zh = file.name.split('.').pop()  # 扩展名 获取
        name = str(random.randint(10000, 99999) + time.time()) + '.' + zh
        try:
            with open(f'./static/myadmin/images/face/{name}', 'wb+') as fp:  # 打开或者创建一个图片 再用write把网页获取到的图片存放到创建的图片中
                # fp.write(file)  # 存放到创建的图片中
                #分块写入
                for chunk in file.chunks():
                    fp.write(chunk)
                filename = f'/static/myadmin/images/face/{name}'
                return filename
        except:
            return False


