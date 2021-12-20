import random

#阿里云
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


from django.contrib.sites import requests
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from django.urls import reverse

from myadmin import models
from django.contrib.auth.hashers import make_password, check_password


#用户中心--主页面(个人信息)
def usercenterinfo(request):
    #接收当前用户
    myuser=request.session.get('myuser')
    userobj=models.Users.objects.get(id=myuser['id'])
    #装入集合
    context={'data':userobj}
    return render(request,'mybook/user_center_info.html',context)

#用户中心--收货地址
def receaddress(request):
    # 接收当前用户信息
    myuser = request.session.get('myuser')
    userobj = models.Users.objects.get(id=myuser['id'])
    if request.method=='POST':
        #接收POST提交的数据
        data=request.POST.dict()
        # 删除token
        data.pop('csrfmiddlewaretoken')
        # 添加当前购买人用户信息
        data['uid']=userobj
        #最多只能拥有两个地址 判断
        if models.ReceivingAddress.objects.filter(uid=userobj).count() >= 2:
            url = reverse('mybook_receaddress')
            return HttpResponse(f'<script>alert("最多只能拥有两个收货地址");location.href="' + url + '" </script>')
        #数据库添加
        obj=models.ReceivingAddress(**data)
        obj.save()
        #跳转
        url = reverse('mybook_receaddress')
        return HttpResponse(f'<script>alert("添加成功");location.href="' + url + '" </script>')
    elif request.method=='GET':
        #查询当前用户的所有收货地址
        data=models.ReceivingAddress.objects.filter(uid=userobj)
        #装入集合
        context={'data':data}
        return render(request,'mybook/user_center_site.html',context)

#修改收货地址默认
def upreceselect(request):
    #接收当前用户
    myuser = request.session.get('myuser')
    userobj = models.Users.objects.get(id=myuser['id'])
    try:
        #把此用户的所有收货地址默认为0
        data=models.ReceivingAddress.objects.filter(uid=userobj)
        for i in data:
            i.receselect=0
            i.save()
        #接收地址id
        id=request.GET.get('receid')
        #修改当前地址 默认属性
        obj=models.ReceivingAddress.objects.get(id=id)
        obj.receselect=1
        obj.save()
        return JsonResponse({'code': 0, 'msg': '修改默认地址成功!'})
    except:
        return JsonResponse({'code': 1, 'msg': '修改默认地址失败!'})

#用户登录
def userlogin(request):
    if request.method=="GET":
        return render(request, 'mybook/login.html')
    elif request.method=="POST":
        #接收post表单
        data=request.POST.dict()
        # 删除token
        data.pop('csrfmiddlewaretoken')
        #查询是否有这个用户
        try:
            obj = models.Users.objects.get(phone=data['phone'])
        except:
            return HttpResponse(f'<script>alert("用户名不存在!");history.back(); </script>')
        #如果存在则验证密码
        if check_password(data['password'],obj.password):
            #登录成功操作 讲用户数据存入session
            request.session['myuser']={'id':obj.id,'phone':obj.phone}
            url = reverse('mybook_index')
            return HttpResponse(f'<script>alert("登录成功");location.href="' + url + '" </script>')
        else:
            return HttpResponse(f'<script>alert("密码错误!");history.go(-1); </script>')

#用户注册
def userregister(request):
    if request.method=='GET':
        return render(request, 'mybook/register.html')
    elif request.method=='POST':
        #接收表单
        # data=request.POST.dict()
        data={}
        data['phone']=request.POST.get('phone')
        data['password']=request.POST.get('password')

        # 删除token
        # data.pop('csrfmiddlewaretoken')
        #从session中获取phone以及vcode
        sessions=request.session.get('vcodes')
        phone = sessions['phone']
        vcode = sessions['vcode']
        #验证手机号以及验证码
        if data['phone']!=phone and data['vcode']!=vcode:
            return HttpResponse(f'<script>alert("手机号码或验证码有错误!");history.back(); </script>')
        # 密码加密
        data['password'] = make_password(data['password'])
        #存入数据库
        obj=models.Users(**data)
        obj.save()
        #注册成功跳转到登陆页面
        url = reverse('mybook_login')
        return HttpResponse(f'<script>alert("注册成功");location.href="' + url + '" </script>')

#用户退出
def userexit(request):
    # flush删除当前会话数据
    #删除单个session del request.session['a'] 不存在就报错
    #清除所有会话session 但不会删除数据库数据 request.session.clear()
    #清除当前的会话数据 数据库也会删除request.session.flush()
    request.session.flush()
    url = reverse('mybook_index')
    return HttpResponse(f'<script>alert("退出成功");location.href="' + url + '" </script>')

#手机号验证
def checkphone(request):
    #接收
    phone=request.GET.get('phone')
    #验证
    obj=models.Users.objects.filter(phone=phone).count()
    #判断
    if obj:
        return JsonResponse({'code':1,'msg':'手机号码已存在'})
    else:
        return JsonResponse({'code': 0, 'msg': '手机号码可以使用'})

#短信验证码
def sendcoke(request):
    # 接收
    phone = request.GET.get('phone')
    #查看手机号码是否已经注册(二次验证码手机号码是否存在)
    obj = models.Users.objects.filter(phone=phone).count()
    # 判断手机号是否存在
    if obj:
        return JsonResponse({'code': 1, 'msg': '手机号码已存在','vcode':''})
    #创建一个验证码vcode
    vcode=random.randint(10000,99999)
    #存入session 注册操作时候进行验证
    request.session['vcodes']={'phone':phone,'vcode':123456}
    #调用发送短信方法
    # res=coke(phone,vcode)
    if True:
        return JsonResponse({'code': 0, 'msg': '短信验证码已发送!', 'vcode': 123456})
    # else:
    #     return JsonResponse({'code': 2, 'msg': '短信验证码发送失败,请重试', 'vcode': ''})



#封装发送短信验证码请求以及响应接收
# def coke(phone,vcode):
#     #请求时的POST数据
#     url='https://open.ucpaas.com/ol/sms/sendsms'
#     data={
#         "PhoneNumbers":phone,
#         "SignName":"阿里云短信测试",
#         "TemplateCode":"测试专用模板",
#         "param":vcode,
#         "mobile":phone
#     }
#     headers={
#         'Content-Type':'application/json'
#     }
#
#     #发送请求
#     response=requests.post(url,json=data,headers=headers)
#     #接收响应
#     res = response.json()
#     #响应格式     示例{"code":"0",
#     #    "msg":"OK",
#     #    "count":"1",
#     #    "create_date":"2017-08-28 19:08:28",
#     #    "uid":"",
#     #    "smsid":"f96f79240e372587e9284cd580d8f953",
#     #    "mobile":"18011984299"
#     #       }
#     #对code和msg进行判断 看短信是否发送成功
#     if res['code']=='000000' and res['msg']=='OK':
#         return True
#     else:
#         return False


