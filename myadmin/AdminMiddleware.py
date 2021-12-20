from django.shortcuts import render
from django.http import HttpResponse
import re
from django.urls import reverse


#中间件:在访问一些路径会执行此方法
class AdminLoginMiddleware:

    #初始响应
    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):

        #检测当前的请求是否登录,如果已经登录则放行,未登录则跳转到登录页
        #获取当前用户的请求路径
        urllist=[reverse('home_yzm'),reverse('home_login')]
        #判断是否进入了后台,并且不是登录界面 排除urllist
        if re.match('/myadmin/',request.path) and request.path not in urllist:

            #检测session中是否有用户数据
            if request.session.get('AdminUser','')=='':
                url=reverse('home_login')
                return HttpResponse('<script>alert("请先登录");location.href="'+url+'"</script>')
        response=self.get_response(request)
        return response