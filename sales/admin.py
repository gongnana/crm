from django.contrib import admin

# Register your models here.

from sales import models


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'email', 'telephone', 'is_active']
    list_editable = ['password', 'email', 'telephone', 'is_active']


admin.site.register(models.UserInfo, UserInfoAdmin)
admin.site.register(models.Customer)
admin.site.register(models.Campuses)
admin.site.register(models.ClassList)
admin.site.register(models.ConsultRecord)
admin.site.register(models.Enrollment)
admin.site.register(models.CourseRecord)
admin.site.register(models.StudyRecord)
