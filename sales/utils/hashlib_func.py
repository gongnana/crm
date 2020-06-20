# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 2020/6/6 17:18
# Author : Eunice

import hashlib


def set_md5(value):
    """
    :param value: 加密的字符串数据
    :return:
    """
    salt = 'username'
    md5_value = hashlib.md5(salt.encode('utf-8'))
    md5_value.update(value.encode('utf-8'))
    return md5_value.hexdigest()