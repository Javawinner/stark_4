from stark.service.v1 import site
from app01 import models
from stark.service.v1 import StarkHandler
from django.conf.urls import url
from django.shortcuts import HttpResponse


class DepartHandler(StarkHandler):
    list_display = ['id', 'title']


class UserInfoHandler(StarkHandler):
    # 定制页面显示的列
    list_display = ['name', 'age', 'email']  # 显示name,age,email列


site.register(models.Depart, handler_class=DepartHandler)
site.register(models.UserInfo, handler_class=UserInfoHandler)
