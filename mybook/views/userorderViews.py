import random
from django.contrib.sites import requests
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render,HttpResponse
from django.urls import reverse
from myadmin import models
from django.contrib.auth.hashers import make_password, check_password

#提交订单页面
def submitorder(request):
    #获取当前用户
    myuser=request.session.get('myuser')
    userobj=models.Users.objects.get(id=myuser['id'])
    # 验证用户是否登录
    if not myuser['id']:
        url = reverse('mybook_login')
        return HttpResponse(f'<script>alert("请先登录");location.href="' + url + '" </script>')



    if request.method=='GET':#表单页面显示
        user=models.Users.objects.get(id=myuser['id'])
        #查询出提交的购物车商品 select=1的 1为选中的
        data=models.ShoppingCart.objects.filter(uid=user,select=1)
        #查询出此订单总价
        countprice=0
        for i in data:
            countprice+=round(i.bid.bkprice*i.number,2)
        #查询此用户的默认收货地址
        receaddressobj=models.ReceivingAddress.objects.filter(uid=userobj)
        #装入集合
        context={'data':data,'countprice':round(countprice,2),'receaddress':receaddressobj}
        return render(request,'mybook/submitorder.html',context)
    elif request.method=='POST':#订单进行提交创建订单
        # 验证用户是否有收货地址
        address = models.ReceivingAddress.objects.filter(uid=userobj).count()
        if not address:
            url = reverse('mybook_receaddress')
            return HttpResponse(f'<script>alert("请先在用户中心添加收货地址!");location.href="' + url + '" </script>')

        #接收post表单提交的数据
        data=request.POST.dict()

        # 删除token
        data.pop('csrfmiddlewaretoken')
        # try:
        #进行数据库创建订单
        #1.购买用户id
        #2.创建订单对象
        data_oroder={}
        data_oroder['uid']=userobj
        try:
            data_oroder['receid']=models.ReceivingAddress.objects.get(id=data['receid'])
        except:
            url = reverse('mybook_receaddress')
            return HttpResponse(f'<script>alert("请选择默认收货地址!");location.href="' + url + '" </script>')
        data_oroder['paymethod']=data['paymethod']
        new_orderobj=models.Order(**data_oroder)
        new_orderobj.save()
        #3.购买的购物车信息
        shoppdata=models.ShoppingCart.objects.filter(uid=myuser['id'],select=1)
        countttttttt = 0
        #4.提取购物车信息里面的商品信息 创建  订单详情对象 并且绑定订单号
        for i in shoppdata:
            data_oroderinfo={}
            data_oroderinfo['oid']=new_orderobj
            data_oroderinfo['bid']=i.bid
            data_oroderinfo['number']=i.number
            # 5.网页返回的总价和后台计算的总价核对
            countttttttt+=round(i.bid.bkprice * i.number,2)
            data_oroderinfo['price']=round(i.bid.bkprice * i.number,2)
            new_orderinfoobj=models.OrderInfo(**data_oroderinfo)
            new_orderinfoobj.save()
            #6.加入之后就将购物车的商品信息删除
            i.delete()
            # 5.网页返回的总价和后台计算的总价核对(2)
        if float(data['price']) != float(round(countttttttt, 2)):
            url = reverse('mybook_suborder')
            return HttpResponse(f'<script>alert("前后台价格不一致!请重试!");location.href="' + url + '" </script>')
        #调用支付宝接口
        return order_pay_request(new_orderobj,float(round(countttttttt, 2)))
        # url = reverse('mybook_cart')
        # return HttpResponse(f'<script>alert("提交订单成功,请支付!");location.href="' + url + '" </script>')
        # except:
        #     url = reverse('mybook_suborder')
        #     return HttpResponse(f'<script>alert("提交订单失败,请支付!");location.href="' + url + '" </script>')


#当前用户所有订单列表显示
def orderlist(request):
    # 获取当前用户
    myuser = request.session.get('myuser')
    userobj = models.Users.objects.get(id=myuser['id'])
    #获取当前用户的所有订单
    data=models.Order.objects.filter(uid=userobj)
    #装入每个订单的总价
    for i in data:
        sum=0
        for y in i.orderinfo_set.all():
            sum+=y.price
        i.countprice=round(sum,2)
    #装入集合
    context={'data':data}
    return render(request,'mybook/user_center_order.html',context)

# 支付宝回调地址
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def pay_result(request):
    print('进来了')
    # 获取对象
    alipay = Get_AliPay_Object()
    if request.method == "POST":
        # 检测是否支付成功
        # 去请求体中获取所有返回的数据：状态/订单号
        from urllib.parse import parse_qs
        # name&age=123....
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        print('------------------开始------------------')
        print('POST验证', status)
        print(post_dict)
        out_trade_no = post_dict['out_trade_no']
        print(out_trade_no)
        # 修改订单状态
        ass = {'paystatus': 1, 'paytime': post_dict['gmt_payment']}
        print(ass)
        # models.Order.objects.filter(ordercode=out_trade_no).update(**ass)
        print('------------------结束------------------')
        # 修改订单状态：获取订单号
        return HttpResponse('success')
    else:
        params = request.GET.dict()
        sign = params.pop('sign', None)
        status = alipay.verify(params, sign)
        print('==================开始==================')
        print('GET验证', status)
        print('==================结束==================')
        return HttpResponse('<script>alert("支付成功");location.href="/order/list"</script>')



# 发起支付请求
def order_pay_request(orderobj,count):
    #商品简单描述
    print(orderobj.orderinfo_set.first().bid.bkname)
    #交易金额
    # 获取支付对象
    alipay = Get_AliPay_Object()
    # 生成支付的url
    query_params = alipay.direct_pay(
        subject=orderobj.orderinfo_set.first().bid.bkname,  # 商品简单描述
        out_trade_no=orderobj.id,  # 用户购买的商品订单号
        total_amount=count,  # 交易金额(单位: 元 保留俩位小数)
    )

    # 支付宝网关地址（沙箱应用）
    pay_url = settings.ALIPAY_URL + "?{0}".format(query_params)
    print(pay_url)
    print('正在发起支付请求...')
    # 页面重定向到支付页面
    return HttpResponseRedirect(pay_url)





# 支付宝对象创建方法
from BookMall import settings
from utils.pay import AliPay


# AliPay 对象实例化
def Get_AliPay_Object():
    alipay = AliPay(
        appid=settings.ALIPAY_APPID,  # APPID （沙箱应用）
        app_notify_url=settings.ALIPAY_NOTIFY_URL,  # 回调通知地址
        return_url=settings.ALIPAY_RETURN_URL,  # 支付完成后的跳转地址
        app_private_key_path=settings.APP_PRIVATE_KEY_PATH,  # 应用私钥
        alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,  # 支付宝公钥
        debug=True,  # 默认False,
    )
    return alipay

