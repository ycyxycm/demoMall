import os
from django.shortcuts import render,HttpResponse
from django.urls import reverse


def index(request):
    return render(request,'myadmin/order/orderindex.html')