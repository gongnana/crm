# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 2020/6/9 16:47
# Author : Eunice


# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Time : 2020/6/8 18:55
# Author : Eunice


from django.conf import settings
from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.views import View
from django.db import transaction
from django.forms.models import modelformset_factory
from django import forms

from sales import models
from sales.utils.page import MyPagenation
from sales.myforms import CustomerForm
from sales.myforms import ConsultRecordForm
from sales.myforms import EnrollRecordForm
# Create your views here.


# 首页
def home(request):
    return render(request, 'saleshtml/home.html')


# 公户私户展示
class CustomerView(View):
    def get(self, request):
        current_request_path = request.path
        # 公户请求
        if current_request_path == reverse('customer'):
            tag = '1'
            customer_list = models.Customer.objects.filter(consultant__isnull=True)
        else:
            tag = '2'
            # 私户请求
            user_obj = request.user_obj
            customer_list = models.Customer.objects.filter(consultant_id=user_obj)
        # 分页和搜索
        base_url = request.path  # 访问的路径
        get_data = request.GET.copy()  # 将request.GET对象改成可修改的
        page_num = request.GET.get('page')  # 获取当前页码数
        search_field = request.GET.get('search_field')  # 选择搜索字段
        kw = request.GET.get('kw')  # 搜索关键字
        if kw:
            kw = kw.strip()
            # customer_list = models.Customer.objects.filter(**{search_field: kw})
            # 另一种实现方式，支持或查询
            q_obj = Q()  # q条件查询的连接符默认是&连接
            q_obj.children.append((search_field, kw))  # 可以拿到一组关键字 Q(qq=kw)
            # q_obj.children.append((search_field2, kw))  # 添加另一组关键字 Q(name=kw)相当于Q(qq=kw)&Q(name=kw)
            # q_obj.connector = 'or' # 修改连接符为or Q(qq=kw)|Q(name=kw)
            customer_list = customer_list.filter(q_obj)

        else:
            customer_list = customer_list
        customer_count = customer_list.count()
        per_page_num = settings.PER_PAGE_NUM
        page_num_show = settings.PAGE_NUM_SHOW
        page_obj = MyPagenation(page_num, customer_count, base_url, get_data,per_page_num, page_num_show)
        customer_obj = customer_list.reverse()[page_obj.cal_start_data: page_obj.cal_end_data]
        # return render(request, 'saleshtml/customers.html', {'customer_obj': customer_obj, 'page_num_count': page_num_range})
        return render(request, 'saleshtml/customers.html',{'customer_obj': customer_obj, 'page_html': page_obj.html_page, 'tag': tag})

    def post(self, request):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')
        if hasattr(self, action):
            ret = getattr(self, action)(request, cids)
            if ret:
                return ret
            return redirect(request.path)  # 不管是公转私还是私转公，都返回请求的页面

    # 公转私
    def public_private(self, request, cids):

        with transaction.atomic():
            customers = models.Customer.objects.filter(pk__in=cids, consultant__isnull=True).select_for_update()
        if customers.count() != len(cids):
            return HttpResponse('已被其他用户选择')
        customers.update(consultant_id=request.session.get('user_id'))

    # 私转公
    def private_public(self, request, cids):

        customers = models.Customer.objects.filter(pk__in=cids, consultant=request.user_obj)
        customers.update(consultant=None)


def add_edit_customer(request, cid=None):
    """
    :param request:
    :param cid: 客户记录id
    :return:
    """
    label = '编辑客户信息' if cid else '添加客户信息'
    customer_obj = models.Customer.objects.filter(pk=cid).first()
    if request.method == 'GET':
        customer_form = CustomerForm(instance=customer_obj)
        return render(request, 'saleshtml/edit_customer.html', {'customer_form': customer_form, 'label': label})

    else:
        nex_url = request.GET.get('next')
        print(nex_url)
        customer_form = CustomerForm(request.POST, instance=customer_obj)
        if customer_form.is_valid():
            customer_form.save()  # 更新数据
            return redirect(nex_url)  # 返回至编辑之前的页面
        else:
            return render(request, 'saleshtml/edit_customer.html', {'customer_form': customer_form, 'label': label})


# 跟进记录管理
class ConsultRecordView(View):
    def get(self, request):
        # 当前登录用户的未删除的跟进记录
        cid = request.GET.get('cid')
        if cid:
            # 如果存在单个id,那么找到的是当前用户的单个客户的跟进记录
            consult_list = models.ConsultRecord.objects.filter(customer_id=cid,consultant=request.user_obj, delete_status=False).order_by('-date')
        else:
            consult_list = models.ConsultRecord.objects.filter(consultant=request.user_obj, delete_status=False).order_by('-date')

        # 分页和搜索
        base_url = request.path  # 访问的路径
        get_data = request.GET.copy()  # 将request.GET对象改成可修改的
        page_num = request.GET.get('page')  # 获取当前页码数
        search_field = request.GET.get('search_field')  # 选择搜索字段
        kw = request.GET.get('kw')  # 搜索关键字
        if kw:
            kw = kw.strip()
            # customer_list = models.Customer.objects.filter(**{search_field: kw})
            # 另一种实现方式，支持或查询
            q_obj = Q()  # q条件查询的连接符默认是&连接
            q_obj.children.append((search_field, kw))  # 可以拿到一组关键字 Q(qq=kw)
            # q_obj.children.append((search_field2, kw))  # 添加另一组关键字 Q(name=kw)相当于Q(qq=kw)&Q(name=kw)
            # q_obj.connector = 'or' # 修改连接符为or Q(qq=kw)|Q(name=kw)
            consult_list = consult_list.filter(q_obj)

        else:
            consult_list = consult_list
        consult_count = consult_list.count()

        per_page_num = settings.PER_PAGE_NUM
        page_num_show = settings.PAGE_NUM_SHOW

        page_obj = MyPagenation(page_num, consult_count, base_url, get_data, per_page_num, page_num_show)
        page_html = page_obj.html_page()
        consult_obj = consult_list.reverse()[page_obj.cal_start_data: page_obj.cal_end_data]

        return render(request, 'saleshtml/consult_record.html', {'consult_list': consult_obj, 'page_html': page_html})
        # return render(request, 'saleshtml/consult_record.html', {'consult_list': consult_list})

    def post(self, request):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')
        if hasattr(self, action):
            consults = models.ConsultRecord.objects.filter(pk__in=cids)
            getattr(self, 'bulk_delete')(request, consults)
            return redirect(request.path)

    def bulk_delete(self, request, consult):
        consult.update(delete_status=True)


# 添加编辑跟进记录
class AddEditConsultView(View):
    def get(self, request, cid=None):
        label = '编辑跟进记录' if cid else '添加跟进记录'
        consult_obj = models.ConsultRecord.objects.filter(pk=cid).first()
        if request.method == 'GET':
            consult_form = ConsultRecordForm(request, instance=consult_obj)
            return render(request, 'saleshtml/add_edit_consult.html', {'consult_form': consult_form, 'label': label})

    def post(self, request, cid=None):
        consult_obj = models.ConsultRecord.objects.filter(pk=cid).first()
        nex_url = request.GET.get('next')
        if not nex_url:
            nex_url = reverse('consult_record')
        consult_form = ConsultRecordForm(request, request.POST, instance=consult_obj)
        if consult_form.is_valid():
            consult_form.save()  # 更新数据
            return redirect(nex_url)  # 返回至编辑之前的页面
        else:
            return render(request, 'saleshtml/add_edit_consult.html', {'consult_form': consult_form})


# 报名表信息表展示
class EnrollmentView(View):

    def get(self, request):
        enrolls = models.Enrollment.objects.filter(customer__consultant=request.user_obj, delete_status=False)
        return render(request, 'saleshtml/enrollments.html', {'enrolls': enrolls})


# 报名记录管理

class AddEditEnrollmentView(View):

    def get(self, request, cid=None):
        label = '编辑报名记录' if cid else '添加报名记录'
        enroll_obj = models.Enrollment.objects.filter(pk=cid).first()
        if request.method == 'GET':
            enroll_form = EnrollRecordForm(request, instance=enroll_obj)
            return render(request, 'saleshtml/add_edit_enroll.html', {'enroll_form': enroll_form, 'label': label})

    def post(self, request, cid=None):
        enroll_obj = models.Enrollment.objects.filter(pk=cid).first()
        nex_url = request.GET.get('next')
        if not nex_url:
            nex_url = reverse('consult_record')
        enroll_form = EnrollRecordForm(request, request.POST, instance=enroll_obj)
        if enroll_form.is_valid():
            enroll_form.save()  # 更新数据
            return redirect(nex_url)  # 返回至编辑之前的页面
        else:
            return render(request, 'saleshtml/add_edit_consult.html', {'enroll_form': enroll_form})


# 课程记录
class CourseRecordView(View):
    def get(self, request):
        course_records = models.CourseRecord.objects.all()
        return render(request, 'saleshtml/course_record.html', {'course_records': course_records})

    def post(self, request):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')
        if hasattr(self, action):
            getattr(self, 'bulk_create_study_record')(request, cids)
        return HttpResponse('ok')

    # 批量生成学习记录
    def bulk_create_study_record(self, request, cids):
        for cid in cids:
            course_record_obj = models.CourseRecord.objects.filter(pk=cid).first()
            # 通过课程记录找到本节的课程所有学生的记录
            students = course_record_obj.re_class.customer_set.filter(status='studying')
            obj_list = []
            for student in students:
                obj = models.StudyRecord(
                    course_record_id=cid,
                    student=student,
                )
                obj_list.append(obj)
            models.StudyRecord.objects.bulk_create(obj_list)


class StudyRecordModelForm(forms.ModelForm):
    class Meta:
        model = models.StudyRecord
        fields = '__all__'


# 学习记录
class StudyRecordView(View):
    def get(self, request, course_record_id):
        # queryset = models.StudyRecord.objects.filter(course_record_id=course_record_id)
        form_cls = modelformset_factory(model=models.StudyRecord, form=StudyRecordModelForm, extra=0)
        study_records = models.StudyRecord.objects.filter(course_record_id=course_record_id)
        formset = form_cls(queryset=study_records)
        return render(request, 'saleshtml/study_record.html', {'formset': formset})

    def post(self, request, course_record_id):
        form_cls = modelformset_factory(model=models.StudyRecord, form=StudyRecordModelForm, extra=0)
        formset = form_cls(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(request.path)
        else:
            return render(request, 'saleshtml/study_record.html', {'formset': formset})
