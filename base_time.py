#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          base_time
   Description:
   Author:             Black Hole
   date:               2020/11/24
-------------------------------------------------
   Change Activity:    2020/11/24:
-------------------------------------------------
"""

__author__ = 'Black Hole'

from datetime import datetime

import arrow


def get_now_str_date() -> str:
    """
    获取当前时间字符串

    Returns: '2020-05-27 15:08:22'
    Class: <class 'str'>
    """
    return arrow.now().format("YYYY-MM-DD HH:mm:ss")


def get_now_datetime() -> datetime:
    """
    获取当前 datetime

    Returns: 2020-11-24 14:51:32.589053+08:00
    Class: <class 'datetime.datetime'>
    """
    return arrow.now().datetime


def long10_to_datetime(time_stamp):
    """
    获取 time_stamp 对应的 datetime
    Args:
        time_stamp: 时间戳

    Input: 1606196547
    Returns: 2020-11-24 14:51:32.589053+08:00
    Class: <class 'datetime.datetime'>

    """
    return arrow.get(time_stamp, tzinfo='local').datetime


def long13_to_datetime(time_stamp):
    """
    获取 time_stamp 对应的 datetime
    Args:
        time_stamp: 时间戳

    Input: 1606196547
    Returns: 2020-11-24 14:51:32.589053+08:00
    Class: <class 'datetime.datetime'>

    """
    time_stamp = time_stamp / 1000
    return long10_to_datetime(time_stamp=time_stamp)


def long10_to_format(time_stamp):
    """
    时间戳转 str
    Args:
        time_stamp: 时间戳
    Input: 1606196547
    Returns: 2020-11-24 13:42:27
    Class: <class 'str'>
    """
    return arrow.get(time_stamp, tzinfo='local').format("YYYY-MM-DD HH:mm:ss")


def long13_to_format(time_stamp):
    """
    时间戳转 str
    Args:
        time_stamp: 时间戳
    Input: 1606196547
    Returns: 2020-11-24 13:42:27
    Class: <class 'str'>
    """
    time_stamp = time_stamp / 1000
    return long10_to_format(time_stamp=time_stamp)


def print_type(obj: object):
    print(obj)
    print(type(obj))


if __name__ == '__main__':
    print_type(long13_to_format(1606196547823))
    pass
