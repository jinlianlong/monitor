#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/16 14:05
# @File    : AlertView.py

from django.http.response import JsonResponse
from django.http import HttpResponse
from config import AlertValue

import sys, json
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


# 更新 alert_info 数据
def update_alert_info(request):
    temperature = request.POST.get('temperature')
    temperature_flag = request.POST.get('temperature_flag')
    ph = request.POST.get('ph')
    ph_flag = request.POST.get('ph_flag')
    pressure = request.POST.get('pressure')
    pressure_flag = request.POST.get('pressure_flag')

    result = dict()
    if (temperature is None and temperature_flag) or (temperature and temperature_flag is None):
        result['alert_info'] = AlertValue.ALERT_INFO
        result['messsage'] = '%s' % ('请同时填写水温的报警点和如何报警',)
        result['result'] = False
        return HttpResponse(content=json.dumps(obj=result, ensure_ascii=False), content_type='application/json',
                            charset='utf-8')
    if (ph is None and ph_flag) or (ph and ph_flag is None):
        result['alert_info'] = AlertValue.ALERT_INFO
        result['messsage'] = '%s' % ('请同时填写水ph值的报警点和如何报警',)
        result['result'] = False
        return HttpResponse(content=json.dumps(obj=result, ensure_ascii=False), content_type='application/json',
                            charset='utf-8')
    if (pressure is None and pressure_flag) or (pressure and pressure_flag is None):
        result['alert_info'] = AlertValue.ALERT_INFO
        result['messsage'] = '%s' % ('请同时填写水压的报警点和如何报警',)
        result['result'] = False
        return HttpResponse(content=json.dumps(obj=result, ensure_ascii=False), content_type='application/json',
                            charset='utf-8')
    if temperature:
        AlertValue.ALERT_INFO['temperature'] = temperature
        AlertValue.ALERT_INFO['temperature_flag'] = True if temperature_flag == 1 else False
    if ph:
        AlertValue.ALERT_INFO['ph'] = ph
        AlertValue.ALERT_INFO['ph_flag'] = True if ph_flag == 1 else False
    if pressure:
        AlertValue.ALERT_INFO['pressure'] = pressure
        AlertValue.ALERT_INFO['pressure_flag'] = True if pressure_flag == 1 else False

    try:
        result['alert_info'] = AlertValue.ALERT_INFO
        result['messsage'] = 'success'
        result['result'] = True
        return JsonResponse(data=result)
    except Exception, e:
        result['alert_info'] = AlertValue.ALERT_INFO
        result['messsage'] = 'fail: %s' % (e.message, )
        result['result'] = False
        return JsonResponse(data=result)


# 直接获取 alert_info 信息
def get_alert_info():
    result = dict()
    result['message'] = 'success'
    result['code'] = 0
    result['data'] = AlertValue.ALERT_INFO
    result['result'] = True
    return JsonResponse(data=result)
