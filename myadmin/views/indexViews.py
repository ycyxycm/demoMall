import hashlib
import os
from django.shortcuts import render,HttpResponse
from django.urls import reverse
from .. import models


def index(request):
    return render(request, 'myadmin/index.html')

#后台登录及验证
def login(request):
    if request.method=='GET':
        return render(request,'myadmin/login.html')
    elif request.method=='POST':
        data=request.POST.dict()
        #删除token
        data.pop('csrfmiddlewaretoken')
        #检测验证码
        yzm = request.session.get('verifycode')
        if data['yzm'].lower()!=yzm.lower():
            return HttpResponse(f'<script>alert("验证码错误!");history.go(-1); </script>')
        #检测账号
        try:
            obj=models.Users.objects.get(phone=data['phone'])
        except:
            return HttpResponse(f'<script>alert("用户名不存在!");history.go(-1); </script>')
        #检测密码
        from django.contrib.auth.hashers import make_password,check_password
        if check_password(data['password'],obj.password):
            # 完成登录操作
            request.session['AdminUser']= {'id':obj.id,'name':obj.nikename,'phone':obj.phone,'face' :obj.face,}#将用户对象存入session
            url = reverse('home_index')
            return HttpResponse(f'<script>alert("登录成功");location.href="' + url + '" </script>')
        else:
            return HttpResponse(f'<script>alert("密码错误!");history.go(-1); </script>')

#用户退出 清楚session
def exit(request):
    #flush删除当前会话数据
    request.session.flush()
    url = reverse('home_login')
    return HttpResponse(f'<script>alert("退出成功");location.href="' + url + '" </script>')


#验证码
def verifycode(request):
    #引入绘图模板
    from PIL import Image,ImageDraw,ImageFont
    #进入随机数函数
    import random
    #定义变量,用于画面的背景色,宽,搞
    bgcolor=(random.randrange(20,100),random.randrange(20,100),255)#背景色
    width=100
    height=25
    #创建画面对象
    im=Image.new('RGB',(width,height),bgcolor)
    #创建画笔对象
    draw=ImageDraw.Draw(im)
    #调用画笔的poin()函数绘制噪点
    for i in range(0,100):
        xy=(random.randrange(0,width),random.randrange(0,height))
        fill=(random.randrange(0,255),255,random.randrange(0,255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1='123456789'
    #随机选取4个值作为验证码
    rand_str=''
    for i in range(0,4):
        rand_str+=str1[random.randrange(0,len(str1))]
    #构造字体对象
    font=ImageFont.truetype('arial.ttf',23)
    #构造字体颜色
    fontcolor=(255,random.randrange(0,255),random.randrange(0,255))
    #绘制4个字
    draw.text((5,2),rand_str[0],font=font,fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session 用于进一步验证
    request.session['verifycode']=rand_str
    #内存文件操作
    import io
    buf=io.BytesIO()
    #将图片保存在内存中,文件类型为png
    im.save(buf,'png')
    #将内存中的图片数据返回给客户端,MIME类型为图片png
    return HttpResponse(buf.getvalue(),'image/png')


#封装MD5加密
def password_md5(msg):
    hl = hashlib.md5()
    hl.update(msg.encode(encoding='utf-8'))
    return hl.hexdigest()
