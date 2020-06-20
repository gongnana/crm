# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 2020/6/9 09:33
# Author : Eunice

from django import template
from django.urls import reverse
from django.http.request import QueryDict

register = template.Library()


@register.simple_tag
def reverse_url(request):
    if request.path == reverse('customer'):
        return '公户信息'
    else:
        return '我的客户信息'


@register.simple_tag
def resole_url(request, url_name, customer_pk):
    next_url = request.get_full_path()  # 编辑保存之后跳转之后
    reverse_url = reverse(url_name, args=(customer_pk,))
    q = QueryDict(mutable=True)
    q['next'] = next_url
    next_url = q.urlencode()
    full_url = reverse_url + '?' + next_url
    return full_url