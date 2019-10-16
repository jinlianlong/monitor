# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import JsonResponse
from django.http import HttpResponse
from utils import DateUtils
from ..models import Water
from ..db.DBServer import WaterDB
from config import AlertValue
import sys, random, json
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


# 根据日期获取水质信息
def get_water_by_date(request):

    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    # print 'start_time: %s\nend_time: %s' % (start_time, end_time, )

    if start_time is None or end_time is None:
        result = dict()
        result['message'] = u'时间日期为空, 请传入查询时间'.encode('utf-8')
        result['code'] = -1
        result['result'] = False
        return HttpResponse(content=json.dumps(obj=result, ensure_ascii=False), content_type='application/json',
                            charset='utf-8')
    try:
        start = DateUtils.convert_str_to_date(str_date=start_time)
        end = DateUtils.convert_str_to_date(str_date=end_time)
        water_list = Water.objects.filter(curTime__range=(start, end))
        if water_list is None or len(water_list) == 0:
            result = dict()
            result['result'] = False
            result['message'] = u'数据为空'
            result['code'] = -1
            return HttpResponse(content=json.dumps(obj=result, ensure_ascii=False), content_type='application/json',
                            charset='utf-8')
        else:
            data_list = list()
            for info in water_list:
                data = dict()
                data['curTime'] = DateUtils.convert_date_to_str(info.curTime)
                data['ph'] = info.ph
                data['pressure'] = info.pressure
                data['temperature'] = info.temperature
                data['electrolytic'] = info.electrolytic
                data_list.append(data)
            result = dict()
            result['result'] = True
            result['message'] = 'success'
            result['code'] = 0
            result['data'] = data_list

            return JsonResponse(data=result, safe=False, status=200)
    except Exception, e:
        result = dict()
        result['message'] = e.message
        result['result'] = False
        result['code'] = -1
        return JsonResponse(data=result)


# 根据日期获取水质信息, 制作 echart 图
def get_water_by_date_chart(request):
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    # print 'start_time: %s\nend_time: %s' % (start_time, end_time, )

    if start_time is None or end_time is None:
        result = dict()
        result['message'] = u'时间日期为空, 请传入查询时间'.encode('utf-8')
        result['code'] = -1
        result['result'] = False
        return HttpResponse(content=json.dumps(obj=result, ensure_ascii=False), content_type='application/json',
                            charset='utf-8')
    try:
        start = DateUtils.convert_str_to_date(str_date=start_time)
        end = DateUtils.convert_str_to_date(str_date=end_time)
        water_list = Water.objects.filter(curTime__range=(start, end))
        if water_list is None or len(water_list) == 0:
            result = dict()
            result['result'] = False
            result['message'] = u'数据为空'
            result['code'] = -1
            return HttpResponse(content=json.dumps(obj=result, ensure_ascii=False), content_type='application/json',
                                charset='utf-8')
        else:
            data = dict()
            x_time = list()
            phs = list()
            pressures = list()
            temperatures = list()
            electrolytics = list()
            for info in water_list:
                x_time.append(DateUtils.convert_date_to_str(info.curTime))
                phs.append(info.ph)
                pressures.append(info.pressure)
                temperatures.append(info.temperature)
                electrolytics.append(info.electrolytic)
            data['x_time'] = x_time
            data['phs'] = phs
            data['pressures'] = pressures
            data['temperatures'] = temperatures
            data['electrolytics'] = electrolytics
            result = dict()
            result['result'] = True
            result['message'] = 'success'
            result['code'] = 0
            result['data'] = data

            return JsonResponse(data=result, safe=False, status=200)
    except Exception, e:
        result = dict()
        result['message'] = e.message
        result['result'] = False
        result['code'] = -1
        return JsonResponse(data=result)


# 根据日期获取水质的最大, 最小, 平均值的数据
def get_specified_water(request):
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    result = dict()
    if start_time is None or end_time is None:
        result['message'] = u'时间日期为空, 请传入查询时间'.encode('utf-8')
        result['code'] = -1
        result['result'] = False
        return HttpResponse(content=json.dumps(obj=result, ensure_ascii=False), content_type='application/json',
                            charset='utf-8')
    try:
        data_obj = WaterDB.get_instance().query_specified_data_by_date(start_time=start_time, end_time=end_time)
        if not data_obj:

            result['message'] = '查询数据为空'
            result['code'] = -1
            result['result'] = False
            return HttpResponse(content=json.dumps(obj=result, ensure_ascii=False), content_type='application/json',
                                charset='utf-8')
        else:
            result['message'] = 'success'
            result['code'] = 0
            result['result'] = True
            data_obj['avg_water_electrolytic'] = True if round(data_obj['avg_water_electrolytic'], 1) > 0.5 else False
            data_obj['avg_water_temperature'] = round(data_obj['avg_water_temperature'], 1)
            data_obj['avg_water_ph'] = round(data_obj['avg_water_ph'], 1)
            result['data'] = data_obj
            return JsonResponse(data=result, safe=False, status=200)
    except Exception, e:
        result = dict()
        result['message'] = e.message
        result['code'] = -1
        result['result'] = False
        return JsonResponse(data=result)


# 获取报警的水质信息数据
def get_alert_water_info(request):
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    result = dict()
    if start_time is None or end_time is None:

        result['message'] = u'时间日期为空, 请传入查询时间'
        result['result'] = False
        result['code'] = -1
        return HttpResponse(content=json.dumps(obj=result, ensure_ascii=False), content_type='application/json',
                            charset='utf-8')
    try:
        water_list = WaterDB.get_instance().query_specified_alert_by_date(start_time=start_time, end_time=end_time,
                                                             alert_info=AlertValue.ALERT_INFO)
        if water_list is None or len(water_list) < 1:
            result['message'] = u'指定时间内, 报警数据为空'
            result['result'] = False
            result['code'] = -1
            return HttpResponse(content=json.dumps(obj=result, ensure_ascii=False), content_type='application/json',
                                charset='utf-8')
        data_list = list()
        for info in water_list:
            data = dict()
            data['curTime'] = DateUtils.convert_date_to_str(info.get('curTime'))
            data['ph'] = info.get('ph')
            data['pressure'] = info.get('pressure')
            data['temperature'] = info.get('temperature')
            data['electrolytic'] = True if info.get('electrolytic') == 1 else False
            data_list.append(data)
        result['message'] = 'success'
        result['result'] = True
        result['code'] = 0
        result['data'] = data_list
        return JsonResponse(data=result, safe=False, status=200)
    except Exception, e:
        result['message'] = e.message
        result['code'] = -1
        result['result'] = False
        return JsonResponse(data=result)


# 获取报警的水质信息数据
def get_alert_water_info_chart(request):
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    result = dict()
    if start_time is None or end_time is None:

        result['message'] = u'时间日期为空, 请传入查询时间'
        result['result'] = False
        result['code'] = -1
        return HttpResponse(content=json.dumps(obj=result, ensure_ascii=False), content_type='application/json',
                            charset='utf-8')
    try:
        water_list = WaterDB.get_instance().query_specified_alert_by_date(start_time=start_time, end_time=end_time,
                                                             alert_info=AlertValue.ALERT_INFO)
        if water_list is None or len(water_list) < 1:
            result['message'] = u'指定时间内, 报警数据为空'
            result['result'] = False
            result['code'] = -1
            return HttpResponse(content=json.dumps(obj=result, ensure_ascii=False), content_type='application/json',
                                charset='utf-8')
        data = dict()
        x_time = list()
        phs = list()
        pressures = list()
        temperatures = list()
        electrolytics = list()
        for info in water_list:
            x_time.append(DateUtils.convert_date_to_str(info.get('curTime')))
            phs.append(info.get('ph'))
            pressures.append(info.get('pressure'))
            temperatures.append(info.get('temperature'))
            electrolytics.append(True if info.get('electrolytic') == 1 else False)
        data['x_time'] = x_time
        data['phs'] = phs
        data['pressures'] = pressures
        data['temperatures'] = temperatures
        data['electrolytics'] = electrolytics
        result['message'] = 'success'
        result['result'] = True
        result['code'] = 0
        result['data'] = data
        return JsonResponse(data=result, safe=False, status=200)
    except Exception, e:
        result['message'] = e.message
        result['code'] = -1
        result['result'] = False
        return JsonResponse(data=result)


# 获取当前水属性数据方法, 用于页面动态显示
def get_current_info():

    data = dict()
    data['ph'] = round(random.uniform(6.7, 7.7), 1)
    data['pressure'] = round(random.uniform(22, 33), 1)
    data['temperature'] = round(random.uniform(12, 15), 1)
    data['electrolytic'] = True if random.sample([0, 1], 1)[0] == 1 else False
    result = dict()
    result['message'] = 'success'
    result['result'] = True
    result['code'] = 0
    result['data'] = data
    return JsonResponse(data=result, status=200)


# 获取对比数据的方法, 页面两个时刻的数据对比
def get_compare_info(request):
    a_time = request.POST.get('a_time')
    b_time = request.POST.get('b_time')
    result = dict()
    if a_time is None or b_time is None:
        result['message'] = u'时间日期为空, 请传入查询时间'.encode('utf-8')
        result['code'] = -1
        result['result'] = False
        return HttpResponse(content=json.dumps(obj=result, ensure_ascii=False), content_type='application/json',
                            charset='utf-8')
    try:
        a = DateUtils.convert_str_to_date(str_date=a_time)
        b = DateUtils.convert_str_to_date(str_date=b_time)
        water_list = Water.objects.filter(curTime__in=[a, b])
        if len(water_list)<2:
            result['message'] = '查询时间数据为空, 请先把指定日期数据添加到数据库中'
            result['code'] = -1
            result['result'] = False
            return HttpResponse(content=json.dumps(obj=result, ensure_ascii=False), content_type='appllication/json',
                                charset='utf-8')
        data_list = list()
        for info in water_list:
            data = dict()
            data['pressure'] = info.pressure
            data['temperature'] = info.temperature
            data['ph'] = info.ph
            data['electrolytic'] = info.electrolytic
            data['curTime'] = DateUtils.convert_date_to_str(info.curTime)
            data_list.append(data)
        result['message'] = 'success'
        result['code'] = 0
        result['result'] = True
        result['data'] = data_list
        return JsonResponse(data=result, status=200, safe=False)
    except Exception, e:

        result['message'] = e.message
        result['result'] = False
        result['code'] = -1

        return JsonResponse(data=result, status=501)