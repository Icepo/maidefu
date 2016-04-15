# coding=utf-8
from __future__ import unicode_literals

from datetime import datetime

from django.db import models


# Create your models here.
# 商品大类
class Catalog(models.Model):
    name = models.CharField(max_length=32)
    sts = models.CharField(max_length=1)
    sts_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)


# 商品种类
class Item(models.Model):
    name = models.CharField(max_length=32)
    unit = models.CharField(max_length=4)
    catalog = models.ForeignKey(Catalog, related_name='item_catalog')
    sts = models.CharField(max_length=1)
    sts_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)


# 门店清单
class Store(models.Model):
    store_id = models.IntegerField(primary_key=True)
    store_name = models.CharField(max_length=64)
    store_manager = models.CharField(max_length=16)
    store_mobile = models.CharField(max_length=32)
    store_tel = models.CharField(max_length=32)
    store_addr = models.CharField(max_length=128)
    sts = models.CharField(max_length=1)
    sts_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)


# 报货批次
class DaliyBatch(models.Model):
    open_id = models.CharField(max_length=32)
    nick_name = models.CharField(max_length=32)
    store = models.ForeignKey(Store, related_name='daliybath_store')
    total = models.IntegerField()
    sts = models.CharField(max_length=1)
    sts_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)


# 报货明细
class DaliyDetail(models.Model):
    open_id = models.CharField(max_length=32)
    nick_name = models.CharField(max_length=32)
    item = models.ForeignKey(Item, related_name='daliy_item')
    num = models.FloatField(max_length=9)
    store = models.ForeignKey(Store, related_name='daliydetail_store')
    batch = models.ForeignKey(DaliyBatch, related_name='daliydetail_daliybatch')
    sts = models.CharField(max_length=1)
    sts_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)


# 员工信息
class Staff(models.Model):
    open_id = models.CharField(max_length=32)
    real_name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    mobile_num = models.CharField(max_length=32)
    sts = models.CharField(max_length=1)
    sts_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)


# 员工与门店的NVN关系
class StaffStoreRel(models.Model):
    staff = models.ForeignKey(Staff, related_name='staff_store_rel')
    store = models.ForeignKey(Store, related_name='store_staff_rel')
    sts = models.CharField(max_length=1)
    sts_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)


# 系统配置信息
class SysConfig(models.Model):
    config_code = models.CharField(max_length=32)
    config_value = models.CharField(max_length=32)
    config_desc = models.CharField(max_length=128, null=True)
    sts = models.CharField(max_length=1)
    sts_date = models.DateTimeField(auto_now_add=True)
    create_date = models.DateTimeField(auto_now_add=True)
