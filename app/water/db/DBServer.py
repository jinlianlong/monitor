#!/usr/bin/python
# coding:utf-8

import pymysql
from DBUtils.PooledDB import PooledDB
from config.AlertValue import DB_INFO

# 表创建
# CREATE TABLE `water` (
#   `water_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '数据的主键id',
#   `cur_time` date DEFAULT NULL COMMENT '当前数据的有效时间',
#   `water_temperature` float(255,0) DEFAULT NULL COMMENT '水的温度(摄氏度)',
#   `water_ph` float(255,0) DEFAULT NULL COMMENT '水的ph值',
#   `water_pressure` float(255,0) DEFAULT NULL COMMENT '水压单位mpa',
#   `water_electrolytic` tinyint(255) DEFAULT NULL COMMENT '0:弱, 1:强',
#   PRIMARY KEY (`water_id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
##############################################################################
# CREATE TABLE `alert` (
#   `alert_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '报警等级主键',
#   `temperature` float(255,0) DEFAULT NULL COMMENT '温度报警点',
#   `ph` float(255,0) DEFAULT NULL COMMENT 'ph报警点',
#   `pressure` float(255,0) DEFAULT NULL COMMENT '水压报警点',
#   `electrolytic` int(1) DEFAULT NULL COMMENT '电解性报警点',
#   PRIMARY KEY (`alert_id`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin

class WaterDB(object):

    __pool = None

    @classmethod
    def get_instance(cls):
        if not hasattr(WaterDB, "_instance"):
            WaterDB._instance = WaterDB()
        return WaterDB._instance

    def __init__(self):
        # 构造函数, 创建数据库连接, 游标
        self._conn = None
        self._cur = None

    # 数据库连接池
    @staticmethod
    def _get_conn():
        if WaterDB.__pool is None:
            data = DB_INFO
            WaterDB.__pool = PooledDB(creator=pymysql, mincached=int(data['min_cached']), maxcached=int(data['max_cached']),
                                     host=data['host'], user=data['user'], passwd=data['password'], db=data['db'],
                                     port=int(data['port']), maxconnections=int(data['max_connections']),
                                     charset=data['charset'])
        return WaterDB.__pool.connection()

    def _init(self):
        self._conn = WaterDB._get_conn()
        self._cur = self._conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 查询一个操作, 查询一个结果
    def _query_one(self, sql):
        self._init()
        try:
            # print 'sql: %s' % (sql, )
            self._cur.execute(sql)
            result = self._cur.fetchone()
        except Exception, e:
            print str(e).replace('(', '').replace(')', '')
            print 'SQL: %s' % (sql,)
            return None
        finally:
            self._dis_conn()
        return result

    # 查询列表操作, 查询一堆结果, 放到一个列表里
    def _query_list(self, sql):
        self._init()
        try:
            self._cur.execute(sql)
            result_list = self._cur.fetchall()
        except Exception, e:
            print e.message
            return None
        finally:
            self._dis_conn()

        return result_list

    # 释放资源
    def _dis_conn(self):
        self._conn.close()
        self._cur.close()

    # 查询指定日期内的水质数据的最大值, 最小值, 平均值
    def query_specified_data_by_date(self, start_time, end_time):
        db = WaterDB.get_instance()
        sql = """
            SELECT
                AVG(water_temperature) as 'avg_water_temperature', MAX(water_temperature) as 'max_water_temperature', 
                    MIN(water_temperature) as 'min_water_temperature', 
                AVG(water_ph) as 'avg_water_ph', MAX(water_ph) AS 'max_water_ph', MIN(water_ph) as 'min_water_ph',
                AVG(water_pressure) as 'avg_water_pressure', MAX(water_pressure) AS 'max_water_pressure', 
                    MIN(water_pressure) as 'min_water_pressure',
                AVG(water_electrolytic) as 'avg_water_electrolytic', 
                    MAX(water_electrolytic) AS 'max_water_electrolytic', 
                    MIN(water_electrolytic) as 'min_water_electrolytic'
            FROM
                water 
            WHERE 
                cur_time BETWEEN '%s' AND '%s'
        """ % (start_time, end_time, )
        result = db._query_one(sql=sql)
        if not result:
            print 'SQL: %s' % (sql, )
            return None
        return result

    # 根据报警点查询历史的所有报警信息
    def query_specified_alert_by_date(self, start_time, end_time, alert_info):
        db = WaterDB.get_instance()
        sql = """
            SELECT
                cur_time as 'curTime', water_temperature as 'temperature', water_ph as 'ph', water_pressure as 'pressure', 
                water_electrolytic as 'electrolytic'
            FROM
                water
            WHERE
                cur_time BETWEEN '%s' AND '%s'
        """ % (start_time, end_time, )
        sql = sql + " AND ("
        symbol = '>=' if alert_info.get('temperature_flag') else '<='
        sql = sql + ' (water_temperature %s %s)' % (symbol, alert_info.get('temperature'), )
        symbol = '>=' if alert_info.get('ph_flag') else '<='
        sql = sql + ' OR (water_ph %s %s)' % (symbol, alert_info.get('ph'), )
        symbol = '>=' if alert_info.get('pressure_flag') else '<='
        sql = sql + ' OR (water_electrolytic %s %s)' % (symbol, alert_info.get('pressure'), )
        sql = sql + ') ORDER BY cur_time ASC'
        # print 'sql: %s' % (sql, )
        result = db._query_list(sql=sql)
        if not result:
            # print 'SQL: %s' % (sql, )
            return None
        return result


if __name__ == '__main__':

    # start_time = '2019-09-25'
    # end_time = '2019-12-31'
    # db = WaterDB.get_instance()
    # print db.query_specified_data_by_date(start_time=start_time, end_time=end_time)

    start_time = '2019-09-25'
    end_time = '2019-12-31'
    db = WaterDB.get_instance()
    from config import AlertValue
    print db.query_specified_alert_by_date(start_time=start_time, end_time=end_time, alert_info=AlertValue.ALERT_INFO)