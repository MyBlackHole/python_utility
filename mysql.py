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
from loguru import logger
from retrying import retry, RetryError

from .base import iteration_is_none
from .entity.results import Results
from .etc.conf import CONFIG

LOCALHOST = CONFIG.MYSQL_INFO


def mysql_decorator(func):
    def connection(*args, **kwargs):
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

    @mysql_decorator
    @retry(wrap_exception=True, stop_max_attempt_number=stop_max_attempt_number, wait_fixed=wait_fixed,
           stop_max_delay=stop_max_delay)
    def select(self, sql, conn=None, cursor=None, database_info=None):
        results = Results()
        try:
            cursor.execute(sql)
            resp = cursor.fetchall()
            results.success = True
            results.resp = resp
        except Exception as e:
            logger.info(e)
        return results

    def execute(self, sql, conn=None, cursor=None, database_info=None):
        results = Results()
        try:
            results.resp = self._execute_db("execute", sql, conn=conn,
                                            cursor=cursor, database_info=database_info)
            results.success = True
        except RetryError as e:
            results.error = e.args[0].value
        return results

    def executemany(self, sql, data, conn=None, cursor=None, database_info=None):
        results = Results()
        try:
            results.resp = self._execute_db("executemany", sql, data, conn=conn,
                                            cursor=cursor, database_info=database_info)
            results.success = True
        except RetryError as e:
            results.error = e.args[0].value
        return results

    @mysql_decorator
    @retry(wrap_exception=True, stop_max_attempt_number=stop_max_attempt_number, wait_fixed=5000,
           stop_max_delay=stop_max_delay)
    def _execute_db(self, func, *args, conn=None, cursor=None, database_info=None):
        rows = getattr(cursor, func)(*args)
        conn.commit()
        return rows
