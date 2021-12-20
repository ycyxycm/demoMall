from django import template
import math


register=template.Library()
#自定义过滤器
@register.filter
def kong_upper(val):
    print('val from template',val)
    return val.upper()

#自定义标签
from django.utils.html import format_html
@register.simple_tag
def jiafa(a,b):
    res=int(a)+int(b)
    return res

#乘法
@register.simple_tag()
def chengjfa(a,b):
    res=a * b
    return round(res,2)

@register.simple_tag
def showpage(num,request):
    '''

    :param num: 最大页
    :request num: 最大页
    :param p: 当前页
    :return:
    '''
    #接收查询条件
    select = request.GET.get('select', None)
    select_text = request.GET.get('select_text', None)

    p=int(request.GET.get('page',1))
    start=p-5
    end=p+4
    if start<=0:
        start=1
        end=11
    if end>num:
        start=num-9
        end=num
    if num <=10:
        start=1
        end=num
    sum=''
    for i in range(start,end+1):
        sum+=f'<a href="?page={ i }&select={select}&select_text={select_text}">{ i }</a>'
    return format_html(sum)

