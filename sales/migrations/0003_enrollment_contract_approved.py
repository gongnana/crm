# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-06-12 00:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_auto_20200609_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollment',
            name='contract_approved',
            field=models.BooleanField(default=False, help_text='在审阅完学员的资料无误后勾选此项，合同即生效', verbose_name='审批通过'),
        ),
    ]
