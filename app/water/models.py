# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
# 水质数据表
class Water(models.Model):
    # 数据的主键id
    id = models.AutoField(auto_created=True, primary_key=True, db_column='water_id')
    # 当前数据的有效时间
    curTime = models.DateField(auto_now=True, db_column='cur_time')
    # 水的温度(摄氏度)
    temperature = models.FloatField(db_column='water_temperature')
    # 水的ph值
    ph = models.FloatField(db_column="water_ph")
    # 水压单位mpa
    pressure = models.FloatField(db_column='water_pressure')
    # 0:弱, 1:强
    electrolytic = models.BooleanField(default=False, db_column='water_electrolytic')

    def __unicode__(self):
        return u'水质数据检测'

    class Meta:
        # 表名
        db_table = 'water'
        # 默认该数据根据主键 id 排序, 升序排序
        ordering = ['curTime']
        # curTime建立唯一索引
        unique_together = ('curTime', )


# 报警点表
class Alert(models.Model):
    # 报警等级主键
    id = models.AutoField(auto_created=True, primary_key=True, db_column='alert_id')
    # 温度报警点
    temperature = models.FloatField(db_column='temperature')
    # ph报警点
    ph = models.FloatField(db_column="ph")
    # 水压报警点
    pressure = models.FloatField(db_column='pressure')
    # 电解性报警点
    electrolytic = models.BooleanField(default=False, db_column='electrolytic')

    def __unicode__(self):
        return u'报警点设置'

    class Meta:
        # 表名
        db_table = 'alert'
