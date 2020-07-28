#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:   base
   Description: 常用工具代码
   Author:      Black Hole
   date:        2020/5/25
-------------------------------------------------
   Change Activity:
                2020/5/25:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import re
import os
import time
import uuid
import math
import hashlib
import threading
from datetime import datetime, timedelta, date

import arrow
from loguru import logger

mutex = threading.Lock()


def str_is_none(text: str) -> bool:
    """
    判断 str 是否为 None 或 ''
    :param text: str
    :return: bool
    """
    if text is None or text == '':
        return True
    else:
        return False


def get_now_date() -> str:
    """
    '2020-05-27 15:08:22'
    :return: str
    """
    return arrow.now().format("YYYY-MM-DD HH:mm:ss")


def str_to_int(string: [int, str]) -> int:
    """
    判断 string 是否是 int 类型
    :param string: [int,str]
    :return: int
    """
    try:
        if isinstance(string, int):
            return string
        return int(string)
    except Exception as e:
        logger.exception(f" error：{e} ")
        return 0


def iteration_is_none(items):
    """
    判断是否可迭代或为 None
    :param items: 对象
    :return: bool
    """
    try:
        if items is None or len(items) <= 0:
            return True
        else:
            return False
    except Exception as e:
        logger.exception(f" error：{e} ")
        return True


def get_uuid() -> str:
    uuid_str = str(uuid.uuid1())
    uuid_str = uuid_str.replace('-', '')
    return uuid_str


def get_md5(text):
    sign = hashlib.md5(text.encode(encoding='UTF-8')).hexdigest()
    return sign


# datetime转时间戳
def datetime_to_long(date_time):
    try:
        if not isinstance(date_time, datetime):
            return 0
        strtime = date_time.strftime('%Y-%m-%d %H:%M:%S')
        time_array = time.strptime(strtime, "%Y-%m-%d %H:%M:%S")
        time_stamp = int(time.mktime(time_array)) * 1000
        return time_stamp
    except:
        return 0


# 获取当前时间时间戳
def get_now_long_time():
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_array = time.strptime(now_time, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array)) * 1000
    return time_stamp


def format_date_str(date_str, model=1):
    str_list = []
    min_datetime_str = str(datetime.now().year) + '0101000000'
    max_datetime_str = str(datetime.now().year) + '1231235959'
    assert len(date_str) % 2 == 0 and len(date_str) >= 4, '输入的时间格式错误或未指定年份'
    if model >= 0:
        if len(date_str) < 8 and len(date_str) > 4:
            if date_str[4:6] == '02':
                if int(date_str[:4]) % 4 == 0:
                    date_str += '29235959'
                else:
                    date_str += '28235959'
            elif date_str[4:6] in ['01', '03', '05', '07', '08', '10', '12']:
                date_str += '31235959'
            elif date_str[4:6] in ['04', '06', '09', '11']:
                date_str += '30235959'
            else:
                raise ValueError('指定的月份错误')
        date_str += max_datetime_str[len(date_str):]
    else:
        date_str += min_datetime_str[len(date_str):]
    for i, c in enumerate(date_str):
        if i in [4, 6]:
            str_list.append('-')
        elif i == 8:
            str_list.append(' ')
        elif i in [10, 12]:
            str_list.append(':')
        str_list.append(c)
    return datetime.strptime(''.join(str_list), '%Y-%m-%d %H:%M:%S')


def datetime_init():
    return datetime.strptime('1970-1-1 0:0:0', "%Y-%m-%d %H:%M:%S")


def check_contain_chinese(content):
    for ch in content.encode('utf-8').decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def long_to_datetime(timeStamp):
    timeStamp = int(timeStamp)
    if len(str(timeStamp)) == 13:
        timeStamp = math.floor(timeStamp / 1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    otherStyleTime = datetime.strptime(otherStyleTime, "%Y-%m-%d %H:%M:%S")
    return otherStyleTime


def read_txt(path, _enconding='utf-8'):
    file = open(path, 'r+', encoding=_enconding)
    lines = file.readlines()
    file.close()
    tostr = 'amp;'.join(lines)
    tostr = tostr.replace('\n', '').lstrip('\ufeff')
    lines = tostr.split('amp;')
    return lines


def write_txt(path, content, mod='a+'):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    file = open(path, mod, encoding='utf-8')
    file.write(content)
    file.close()


def dict_to_object(py_data, obj, obj_dict={}):
    # py_data = json.loads(json_data)
    dic2class(py_data, obj, obj_dict)
    return obj


def dic2class(py_data, obj, obj_dict):
    for name in [name for name in dir(obj) if not name.startswith('_')]:
        if name not in py_data:
            value = getattr(obj, name)
            setattr(obj, name, value)
        else:
            value = getattr(obj, name)
            setattr(obj, name, set_value(name, value, py_data[name], obj_dict))


def set_value(name, value, py_data, obj_dict):
    # value 为自定义类
    if str(type(value)).__contains__('.'):
        if isinstance(value, datetime):
            if not isinstance(py_data, datetime):
                return datetime.strptime(py_data, '%Y-%m-%d %H:%M:%S')
            else:
                return py_data
            # setattr(obj, name, py_data)
        else:
            dic2class(py_data, value, obj_dict)
    elif str(type(value)) == "<class 'list'>":
        if name in obj_dict.keys():
            child_value_type = type(obj_dict[name])
            value.clear()
            for child_py_data in py_data:
                child_value = child_value_type()
                child_value = set_value(name, child_value, child_py_data, obj_dict)
                value.append(child_value)
        else:
            value = py_data
    else:
        if isinstance(py_data, str) and len(py_data) == 19:
            if re.search(
                    '^(([0-9]{3}[1-9]|[0-9]{2}[1-9][0-9]{1}|[0-9]{1}[1-9][0-9]{2}|[1-9][0-9]{3})-(((0[13578]|1[02])-(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))|((([0-9]{2})(0[48]|[2468][048]|[13579][26])|((0[48]|[2468][048]|[3579][26])00))-02-29)',
                    py_data) is not None:
                value = str_to_datetime(py_data)
                return value

        value = py_data
    return value


def object_to_dict(obj):
    try:
        obj_dict = dict((name, getattr(obj, name)) for name in dir(obj) if not name.startswith('__'))
        return obj_dict
    except:
        return None


def str_to_datetime(str_time):
    try:
        if isinstance(str_time, datetime):
            return str_time
        str_time = str_time.replace('/', '-')
        return datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')
    except:
        return datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')


def datetime_to_str(date_time, time_str='%Y-%m-%d %H:%M:%S'):
    try:
        return date_time.strftime(time_str)
    except:
        return ''


def timedelta_addyear(date_time, add_year):
    year = date_time.year
    month = date_time.month
    day = date_time.day
    hour = date_time.hour
    minute = date_time.minute
    second = date_time.second

    if (year + add_year) % 4 != 0:
        if month == 2:
            if day == 29:
                return datetime.strptime(fill_datetime(year + add_year, month, 28, hour, minute, second),
                                         '%Y-%m-%d %H:%M:%S')

    return datetime.strptime(fill_datetime(year + add_year, month, day, hour, minute, second),
                             '%Y-%m-%d %H:%M:%S')


def fill_datetime(year, month, day, hour, minute, second):
    if len(str(month)) == 1:
        month = '0' + str(month)
    if len(str(day)) == 1:
        day = '0' + str(day)
    if len(str(hour)) == 1:
        hour = '0' + str(hour)
    if len(str(minute)) == 1:
        minute = '0' + str(minute)
    if len(str(second)) == 1:
        second = '0' + str(second)
    return '{0}-{1}-{2} {3}:{4}:{5}'.format(year, month, day, hour, minute, second)


def index_of_str(s1, s2, start_index=0):
    new_s1 = s1[start_index:]
    n1 = len(new_s1)
    n2 = len(s2)
    for i in range(n1 - n2 + 1):
        if new_s1[i:i + n2] == s2:
            return i + start_index
    else:
        return -1


def last_index(s1, s2):
    new_s1 = s1[::-1]
    new_s2 = s2[::-1]
    n1 = len(s1)
    n2 = len(s2)
    for i in range(n1 - n2 + 1):
        if new_s1[i:i + n2] == new_s2:
            return i
    else:
        return -1


def can_json_encoder(old_obj):
    obj = old_obj
    if isinstance(obj, datetime):
        obj = obj.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(obj, date):
        obj = obj.strftime('%Y-%m-%d')

    if isinstance(obj, list):
        new_list = obj.copy()
        for k in range(len(new_list)):
            new_list[k] = can_json_encoder(new_list[k])
        obj = new_list
    if isinstance(obj, dict):
        new_dict = obj.copy()
        for key in new_dict:
            new_dict[key] = can_json_encoder(new_dict[key])
        obj = new_dict
    if check_object(obj):
        obj_dict = dict((name, getattr(obj, name)) for name in dir(obj) if not name.startswith('__'))
        obj = can_json_encoder(obj_dict)
    elif othor_type(obj):
        obj = str(obj)
    return obj


def check_object(obj):
    if obj.__class__.__name__ != 'type' and obj.__class__.__name__ != 'module' and hasattr(obj, '__dict__'):
        return True
    else:
        return False


def othor_type(obj):
    conditions = [datetime, date, int, str, float, list, bool, dict]
    if any(isinstance(obj, c) for c in conditions):
        return False
    else:
        return True
