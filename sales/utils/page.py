# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 2020/6/7 18:38
# Author : Eunice

import re

from django.utils.safestring import mark_safe


class MyPagenation(object):
    def __init__(self, page_num, total_count, base_url,get_data=None, per_page_num=10, page_num_show=5):
        """
        :param page_num: 当前页码数
        :param total_count: 总的数据量
        :param base_url: 基本路径
        :param per_page_num: 每页显示的行数
        :param get_data: 搜索时的参数，QueryDict对象
        """
        self.get_data = get_data  # 搜索条件
        self.per_page_num = per_page_num  # 每页显示10行数据
        self.page_num_show = page_num_show  # 页面生成分页页码的数量
        self.base_url = base_url

        # 兼容当前页码数
        try:
            page_num = int(page_num)
        except Exception:
            page_num = 1
        self.page_num = page_num  # 当前页码数
        quotient, remainder = divmod(total_count, self.per_page_num)  # quotient商, remainder余数

        # 总页码数
        if remainder:
            page_num_count = quotient + 1  # 有余数 页数+1
        else:
            page_num_count = quotient
        self.page_num_count = page_num_count

        if self.page_num < 0:
            self.page_num = 1

        elif self.page_num > self.page_num_count:  # 兼容输入大于总页码的值
            self.page_num = self.page_num_count  # 返回最后一页

        half_num = self.page_num_show // 2
        """
        3 4 5 6 7    5 6 7 8 9 
        """
        if self.page_num - half_num <= 0:  # 页码为负数时
            start_num = 1
            end_num = self.page_num_show+1  # 显示分页的
        elif self.page_num + half_num > self.page_num_count:  # 页码大于总的页码数
            start_num = self.page_num_count - self.page_num_show + 1
            end_num = self.page_num_count + 1

        else:
            start_num = self.page_num - half_num  # 开始页码
            end_num = self.page_num + half_num + 1  # 结束页码

        if self.page_num_count < self.page_num_show:  # 总的页码数小于展示的页码数
            start_num = 1
            end_num = self.page_num_count + 1
        self.start_num = start_num
        self.end_num = end_num


    @property
    def cal_start_data(self):

        return (self.page_num - 1) * self.per_page_num

    @property
    def cal_end_data(self):
        return self.page_num * self.per_page_num

    def html_page(self):
        page_num_range = range(self.start_num, self.end_num)
        page_html = ''

        page_pre_html = '<nav aria-label="Page navigation"><ul class="pagination">'
        page_html += page_pre_html
        self.get_data['page'] = 1
        first_page_html = '<li><a href="{0}?{1}" aria-label="Previous"><span aria-hidden="true">首页</span></a></li>'.format(self.base_url, self.get_data.urlencode())  # 首页标签
        page_html += first_page_html
        if self.page_num <= 1:
            pre_page = '<li class="disabled"><a href="javascript: void(0)" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'  # 如果当前页在第一页上，上一页的标签不能点击
        else:
            # pre_page = '<li><a href="{1}?page={2}{0}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(self.page_num - 1, self.base_url, re.sub('page=\d+', '', self.get_data) if 'page=' in self.get_data else self.get_data + '&')  # 上一页的标签，三元运算符判断是否含有page字段
            self.get_data['page'] = self.page_num - 1
            pre_page = '<li><a href="{1}?{0}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(self.get_data.urlencode(), self.base_url,)
        page_html += pre_page
        for i in page_num_range:
            if self.page_num == i:
                self.get_data['page'] = i
                page_html += '<li class="active"><a href="{1}?{2}">{0}</a></li>'.format(i, self.base_url, self.get_data.urlencode())
            else:
                self.get_data['page'] = i
                page_html += '<li><a href="{1}?{2}">{0}</a></li>'.format(i, self.base_url, self.get_data.urlencode())

        if self.page_num >= self.page_num_count:
            nex_page = '<li class="disabled"><a href="javascript: void(0)" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'  # 下一页的标签
        else:
            self.get_data['page'] = self.page_num + 1
            nex_page = '<li><a href="{1}?{0}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(self.get_data.urlencode(), self.base_url)  # 下一页的标签
        page_html += nex_page
        page_next_html = '</ul></nav>'
        self.get_data['page'] = self.page_num_count
        last_page_html = '<li><a href="{1}?{0}" aria-label="Previous"><span aria-hidden="true">最后一页</span></a></li>'.format(self.get_data.urlencode(), self.base_url)  # 尾页标签
        page_html += last_page_html
        page_html += page_next_html
        return mark_safe(page_html)
