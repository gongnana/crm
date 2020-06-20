# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 2020/6/7 10:28
# Author : Eunice

import os
import random

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRM.settings")
    import django
    django.setup()
    from sales import models

    source_type = (('qq', 'qq群'),
                   ('referral', '内部转介绍'),
                   ('website', '官方网站'),
                   ('baidu_ads', '百度推广'),
                   ('office_direct', '直接上门'),
                   ('WoM', '口碑'),
                   ('public_class', '公开课'),
                   ('website_friends', '友链'),
                   ('other', '其他'),
                   )

    course_choices = (('Linux', 'Linux中高级'),
                      ('PythonFullStack', 'python高级全栈开发'))

    obj_list = []
    for i in range(151):
        d = {
            'qq': str(11+i),
            'name': '阿%s' % i,
            'source': source_type[random.randint(0, 8)][0],
            'course': course_choices[random.randint(0, 1)][0],
        }
        obj = models.Customer(**d)  # 创建customer对象
        obj_list.append(obj)
    models.Customer.objects.bulk_create(obj_list)
