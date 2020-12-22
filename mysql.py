#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:   mysql
   Description:
   Author:      Black Hole
   date:        2020/5/18
-------------------------------------------------
   Change Activity:
                2020/5/18:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import pymysql
from retrying import retry

from .base import iteration_is_none
from .base_er import exception
from .entity.results import Results
from .etc.conf import BaseConfig


def mysql_decorator(func):
    def connection(*args, **kwargs):
        LOCALHOST = BaseConfig.MYSQL_INFO
        database_info = kwargs.get('database_info', LOCALHOST)
        database_info = LOCALHOST if iteration_is_none(database_info) else database_info
        assert all(key in database_info.keys() for key in ['host', 'user', 'password', 'database', 'port']), \
            "数据库信息缺少必要key  'host','user','password','database','port'"
        conn = pymysql.connect(**database_info, cursorclass=pymysql.cursors.DictCursor, read_timeout=30,
                               write_timeout=30)
        cursor = conn.cursor()

        def wrapper(*args, **kwargs):
            kwargs['conn'] = conn
            kwargs['cursor'] = cursor
            return func(*args, **kwargs)

        results = wrapper(*args, **kwargs)
        cursor.close()
        conn.close()
        return results

    return connection


class MySQLManage(object):
    mysql_utility = None
    stop_max_attempt_number = 3
    stop_max_delay = 1500
    wait_fixed = 500

    def __init__(self, stop_max_attempt_number=stop_max_attempt_number, wait_fixed=wait_fixed,
                 stop_max_delay=stop_max_delay):
        self.stop_max_attempt_number = stop_max_attempt_number
        self.stop_max_delay = stop_max_delay
        self.wait_fixed = wait_fixed

    def __new__(cls, *args, **kwargs):
        if cls.mysql_utility is None:
            cls.mysql_utility = object.__new__(cls, *args, **kwargs)
        return cls.mysql_utility

    def select(self, sql: str, conn=None, cursor=None, database_info=None):
        results = Results()
        try:
            results.resp = self._execute_db("execute", sql, conn=conn,
                                            cursor=cursor, fetchall=True, database_info=database_info)
            results.success = True
        except Exception as e:
            return exception(results=results, error=e, info=sql)
        return results

    def execute(self, sql, conn=None, cursor=None, database_info=None):
        results = Results()
        try:
            results.resp = self._execute_db("execute", sql, conn=conn,
                                            cursor=cursor, database_info=database_info)
            results.success = True
        except Exception as e:
            return exception(results=results, error=e, info=sql)
        return results

    def executemany(self, sql, data, conn=None, cursor=None, database_info=None):
        results = Results()
        try:
            results.resp = self._execute_db("executemany", sql, data, conn=conn,
                                            cursor=cursor, database_info=database_info)
            results.success = True
        except Exception as e:
            return exception(results=results, error=e, info=sql)
        return results

    @mysql_decorator
    @retry(stop_max_attempt_number=stop_max_attempt_number, wait_fixed=5000,
           stop_max_delay=stop_max_delay)
    def _execute_db(self, func: str, *args, conn=None, cursor=None, fetchall: bool = False, database_info=None):
        rows = getattr(cursor, func)(*args)
        if fetchall:
            rows = cursor.fetchall()
        else:
            conn.commit()
        return rows
