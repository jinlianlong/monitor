#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/16 13:09
# @File    : DateUtils.py

# 将 %Y-%m-%d 字符串转成 datetime 对象
import datetime
DEFINE_DATE_STR = '%Y-%m-%d'


# 将 字符串 转成 日期
def convert_str_to_date(str_date):
    return datetime.datetime.strptime(str_date, DEFINE_DATE_STR)


# 将 日期 转成 字符串
def convert_date_to_str(obj_date):
    return datetime.datetime.strftime(obj_date, DEFINE_DATE_STR)