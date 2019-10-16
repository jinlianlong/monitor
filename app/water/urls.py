#!/usr/bin/python
# coding:utf-8

from django.conf.urls import url
import views

urlpatterns = [
    # 获取指定时间水属性值得接口地址
    url(regex=r'^getWaterInfos$', view=views.get_water_info_list, name='getWaterInfos'),
    # 获取指定时间水属性值得接口地址, 制作 echart 图
    url(regex=r'^getWaterInfosChart$', view=views.get_water_info_list_chart, name='getWaterInfosChart'),
    # 获取指定时间水属性的最大值, 最小值, 平均值得接口地址
    url(regex=r'^getSpecifiedWaterInfo$', view=views.get_water_specified_info, name='getWaterInfoSpecified'),
    # 获取报警数据
    url(regex=r'^getAlertWaterInfos$', view=views.get_water_alert_info, name='getAlertWaterInfo'),
    # 获取报警数据, 制作 echart 图
    url(regex=r'^getAlertWaterInfosChart$', view=views.get_water_alert_info, name='getAlertWaterInfo'),
    # 获取报警阈值的数据
    url(regex=r'^getAlertInfo$', view=views.get_alert_info, name='getAlertInfo'),
    # 更新报警阈值的数据
    url(regex=r'^updateAlertPoint$', view=views.update_alert_info, name='updateAlertInfo'),
    # 获取动态水质信息接口
    url(regex=r'^getDynamicWaterInfo$', view=views.get_dynamic_water_info, name='getDynamicInfo'),
    # 两个时刻的数据对比
    url(regex=r'^compareWaterInfo$', view=views.get_two_water_compare, name='getCompareWater')
]
