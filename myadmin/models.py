from django.db import models

class Users(models.Model):
    #id,手机号,密码,头像
    phone=models.CharField(max_length=11)
    password=models.CharField(max_length=80)
    face=models.CharField(max_length=100,default='/static/myadmin/images/face/default_face.jpg')
    #昵称,居住地址,性别,身份类型
    nikename=models.CharField(max_length=20,null=True)
    homeaddress = models.CharField(max_length=100,null=True)
    sex = models.CharField(max_length=1,null=True)
    usertype = models.CharField(max_length=50)

class BookType(models.Model):
    #id
    #分类名
    typename=models.CharField(max_length=20)
    #父级id
    fid=models.IntegerField()
    #path
    path=models.CharField(max_length=50)

class Books(models.Model):
    '''
    书名,推荐语,简介,作者
	出版社 出版时间 价格
	所属分类:
	 封面图:
    '''
    #id
    #书名
    bkname=models.CharField(max_length=40)
    #推荐语
    bkreco=models.CharField(max_length=50)
    #简介
    bkbrief=models.CharField(max_length=500)
    #作者
    bkauthor=models.CharField(max_length=30)
    #出版社
    bkpress=models.CharField(max_length=40)
    #出版时间
    bktime=models.DateField()
    #价格
    bkprice=models.FloatField()
    #所属分类
    bktypeid=models.ManyToManyField(to='BookType')


    #封面图 外键1对多      多:图集表 一:图书表
class BooksImgs(models.Model):
    #编号
    #图片url 存放图片
    imgurl=models.ImageField(upload_to='static/myadmin/images/book/')
    #图书id
    imgbkid=models.ForeignKey(to='Books',on_delete=models.CASCADE,)


class ShoppingCart(models.Model):
    #编号
    #图书id
    bid=models.ForeignKey('Books',on_delete=models.CASCADE,)
    #用户id
    uid = models.ForeignKey('Users', on_delete=models.CASCADE, )
    #数量
    number=models.IntegerField()
    #是否选中 0未选中 1选中
    select=models.IntegerField(default=0)

class ReceivingAddress(models.Model):
    #编号
    #收货人
    recename=models.CharField(max_length=30)
    #收货电话
    recephone=models.CharField(max_length=11)
    #收货地址
    receaddress=models.CharField(max_length=100)
    #购买人id
    uid=models.ForeignKey('Users', on_delete=models.CASCADE, )
    # 是否默认 0未选中 1选中
    receselect = models.IntegerField(default=0)

class Order(models.Model):
    #编号(订单号)
    #用户id
    uid=models.ForeignKey('Users', on_delete=models.CASCADE, )
    #收货地址id
    receid=models.ForeignKey('ReceivingAddress',on_delete=models.CASCADE,)
    #支付方式 0货到付款 1微信 2支付宝 3银行卡
    paymethod=models.IntegerField(default=0)
    #订单状态 0 未支付 1已支付 2已发货 3已收货 4取消
    state=models.IntegerField(default=0)
    #订单创建时间
    ordertime=models.DateTimeField(auto_now_add=True) #自动创建当前时间
    #订单支付时间
    paytime=models.DateTimeField(null=True)


class OrderInfo(models.Model):
    #编号
    #订单id
    oid=models.ForeignKey('Order', on_delete=models.CASCADE, )
    #图书id
    bid=models.ForeignKey('Books',on_delete=models.CASCADE,)
    #数量
    number=models.IntegerField()
    # 订单总价
    price = models.FloatField()