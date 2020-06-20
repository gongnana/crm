# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 2020/6/9 16:28
# Author : Eunice

from django.shortcuts import render, redirect
from django.urls import reverse


from sales import models
from sales.utils.hashlib_func import set_md5
from sales.myforms import RegisterForm

# 登录功能
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = models.UserInfo.objects.filter(username=username, password=set_md5(password)).first()
        if user_obj:
            # 将用户信息保存到session中
            request.session['user_id'] = user_obj.pk
            return redirect('customer')
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误，请重新登录'})


# 注册功能
def register(request):
    if request.method == 'GET':
        register_form_obj = RegisterForm()
        return render(request, 'register.html', {'register_form_obj': register_form_obj})
    else:
        register_form_obj = RegisterForm(request.POST)
        if register_form_obj.is_valid():
            register_form_obj.cleaned_data.pop('r_password')
            password = register_form_obj.cleaned_data.pop('password')
            # 更新加密后的密码
            register_form_obj.cleaned_data.update({'password': set_md5(password)})
            # print(register_form_obj.cleaned_data)
            models.UserInfo.objects.create(**register_form_obj.cleaned_data)
            return redirect('login')
        else:
            return render(request, 'register.html', {'register_form_obj': register_form_obj})
