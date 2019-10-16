#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/16 15:43
# @File    : AlertValue.py

# 报警点写在内存里, 写在数据库里就一条数据不值当, 给一个默认值
ALERT_INFO = dict()
ALERT_INFO['temperature'] = 15
ALERT_INFO['temperature_flag'] = True
ALERT_INFO['ph'] = 7
ALERT_INFO['ph_flag'] = True
ALERT_INFO['pressure'] = 22
ALERT_INFO['pressure_flag'] = True


DB_INFO = dict()
DB_INFO['host'] = 'rm-wz95t7r1kxw72u800yo.mysql.rds.aliyuncs.com'
DB_INFO['port'] = '3306'
DB_INFO['db'] = 'monitor'
DB_INFO['user'] = 'root'
DB_INFO['password'] = 'descendant_123'
DB_INFO['charset'] = 'utf8'
DB_INFO['min_cached'] = '5'
DB_INFO['max_cached'] = '20'
DB_INFO['max_connections'] = '30'
