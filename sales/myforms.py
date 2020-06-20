# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 2020/6/9 16:30
# Author : Eunice

import re

from django import forms
from django.forms.fields import DateField
from multiselectfield.forms.fields import MultiSelectFormField
from django.core.exceptions import ValidationError

from sales import models


# 自定义手机号码验证规则
def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号格式错误')  # 自定义验证规则的时候，需要手动抛出错误


# 注册modelform相关验证
class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=16,
        min_length=6,
        widget=forms.TextInput(attrs={'class': 'username', 'placeholder': '您的用户名', 'autocomplete': 'off'}),
        error_messages={'required': '用户名不能为空',
                        'max_length': '用户名不能大于16位',
                        'min_length': '用户名不能小于6位'}
    )

    password = forms.CharField(
        label='密码',
        max_length=32,
        min_length=6,
        widget=forms.PasswordInput(attrs={'class': 'password', 'placeholder': '输入密码', 'oncontextmenu': 'return false',
                                          'onpaste': 'return false'}),
        error_messages={'required': '密码不能为空',
                        'max_length': '密码不能大于32位',
                        'min_length': '用户名不能小于6位'}
    )

    r_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class': 'password', 'placeholder': '再次输入密码', 'oncontextmenu': 'return false',
                                          'onpaste': 'return false'}),
        error_messages={'required': '确认密码不能为空'}
    )
    email = forms.EmailField(
        label='邮箱',
        error_messages={
            'required': '确认密码不能为空',
            'invalid': '邮箱格式不对'
        },
        widget=forms.EmailInput(
            attrs={'type': 'email', 'class': 'email', 'placeholder': '输入邮箱地址', 'oncontextmenu': 'return false',
                   'onpaste': 'return false'})
    )
    telephone = forms.CharField(
        label='电话号码',
        validators=[mobile_validate],
        error_messages={
            'required': '电话号码不能为空',
            'invalid': '电话格式不对'
        },
        widget=forms.TextInput(attrs={'class': 'phone_number', 'placeholder': '输入手机号码', 'autocomplete': 'off', })
    )

    def clean(self):
        value = self.cleaned_data
        rp = value.get('r_password')
        p = value.get('password')
        if p == rp:
            return value
        else:
            self.add_error('r_password', '两次输入的密码不一致')
            raise ValidationError('两次输入的密码不一致')


# 客户信息相关验证
class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'

        error_messages = {
            'qq': {'required': '不能为空'},
            'course': {'required': '不能为空'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            print(type(field))
            if not isinstance(field, MultiSelectFormField):
                field.widget.attrs.update({'class': 'form-control'})

            if isinstance(field, DateField):
                field.widget.attrs.update({'type': 'date'})


class ConsultRecordForm(forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'
        exclude = ['delete_status', ]

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'customer':
                field.queryset = models.Customer.objects.filter(consultant=request.user_obj)  # 筛选出当前登录用户的咨询客户
            elif field_name == 'consultant':
                # field.queryset = models.UserInfo.objects.filter(pk=request.user_obj.pk)  # 跟进人仅为当前登录用户
                field.choices = ((request.user_obj.pk, request.user_obj.username),)


class EnrollRecordForm(forms.ModelForm):
    class Meta:
        model = models.Enrollment
        fields = '__all__'

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})