# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.http import require_http_methods
from view import WaterView, AlertView


# 根据时间获取水质数据, 列表
# start_time: %Y-%m-%d 请求指定数据的开始时间
# end_time: %Y-%m-%d 请求制定数据的结束时间
@require_http_methods(['POST'])
def get_water_info_list(request):
    return WaterView.get_water_by_date(request=request)

# 根据时间获取水质数据, echart 图
# start_time: %Y-%m-%d 请求指定数据的开始时间
# end_time: %Y-%m-%d 请求制定数据的结束时间
@require_http_methods(['POST'])
def get_water_info_list_chart(request):
    return WaterView.get_water_by_date_chart(request)

# 根据时间获取水质的最大, 最小, 平局的数据
# start_time: %Y-%m-%d 请求指定数据的开始时间
# end_time: %Y-%m-%d 请求制定数据的结束时间
@require_http_methods(['POST'])
def get_water_specified_info(request):
    return WaterView.get_specified_water(request=request)

# 根据时间获取水质的报警信息数据
# start_time: %Y-%m-%d 请求指定数据的开始时间
# end_time: %Y-%m-%d 请求制定数据的结束时间
@require_http_methods(['POST'])
def get_water_alert_info(request):
    return WaterView.get_alert_water_info(request=request)

# 根据时间获取水质的报警信息数据
# start_time: %Y-%m-%d 请求指定数据的开始时间
# end_time: %Y-%m-%d 请求制定数据的结束时间
@require_http_methods(['POST'])
def get_water_alert_info_chart(request):
    return WaterView.get_alert_water_info_chart(request=request)

# 设置报警值
# temperature: double 水温摄氏度
# ph: double 水的ph值
# pressure: double 水压Mpa
@require_http_methods(['POST'])
def update_alert_info(request):
    return AlertView.update_alert_info(request=request)


# 获取当前报警点的值
@require_http_methods(['POST', 'GET'])
def get_alert_info(request):
    return AlertView.get_alert_info()


# 获取水质的当前数据
@require_http_methods(['POST', 'GET'])
def get_dynamic_water_info(request):
    return WaterView.get_current_info()


# 两个时刻数据对比
@require_http_methods(['POST'])
def get_two_water_compare(request):
    return WaterView.get_compare_info(request)