from django.conf.urls import url
from django.contrib import admin
from sales import views

from sales.views import auth
from sales.views import customer

urlpatterns = [
    # 登录
    url(r'^login/', auth.login, name='login'),

    # 注册
    url(r'^register/', auth.register, name='register'),

    # 首页
    url(r'^home/', customer.home, name='home'),

    # 客户
    url(r'^customer/', customer.CustomerView.as_view(), name='customer'),

    # 我的客户
    url(r'^mycustomer/', customer.CustomerView.as_view(), name='mycustomer'),

    # 添加客户
    # url(r'^add_customer/', views.add_customer, name='add_customer'),
    url(r'^add_customer/', customer.add_edit_customer, name='add_customer'),

    # 编辑客户信息
    # url(r'^edit_customer/(\d+)/', views.edit_customer, name='edit_customer'),
    url(r'^edit_customer/(\d+)/', customer.add_edit_customer, name='edit_customer'),

    # 跟进记录展示
    url(r'^consult_record/', customer.ConsultRecordView.as_view(), name='consult_record'),

    # 添加跟进记录
    url(r'^add_consult_record/', customer.AddEditConsultView.as_view(), name='add_consult_record'),

    # 编辑跟进记录
    url(r'^edit_consult_record/(\d+)/', customer.AddEditConsultView.as_view(), name='edit_consult_record'),

    # 报名表信息展示
    url(r'^enrollment/', customer.EnrollmentView.as_view(), name='enrollment'),

    # 添加报名记录
    url(r'^enroll_add/', customer.AddEditEnrollmentView.as_view(), name='enroll_add'),

    # 编辑报名记录
    url(r'^enroll_edit/(\d+)/', customer.AddEditEnrollmentView.as_view(), name='enroll_edit'),

    # 课程记录
    url(r'^course_record/', customer.CourseRecordView.as_view(), name='course_record'),

    # 查看学习记录
    url(r'^study_record/(\d+)', customer.StudyRecordView.as_view(), name='study_record'),

]
