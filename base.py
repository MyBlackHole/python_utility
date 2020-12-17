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

import hashlib
import json
import math
import os
import pickle
import re
import threading
import time
import uuid
from datetime import datetime, date
from pathlib import Path
from urllib import parse

import psutil
from loguru import logger

# 线程锁
mutex = threading.Lock()


def get_now_datetime():
    return datetime.now().replace(microsecond=0)


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
        logger.info(f" error：{e} ")
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


def get_uuid3(_str: str) -> str:
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, _str)).replace("-", "")


def get_md5(text):
    sign = hashlib.md5(text.encode(encoding='UTF-8')).hexdigest()
    return sign


# datetime转时间戳
def datetime_to_long(date_time):
    try:
        if isinstance(date_time, int):
            if len(str(date_time)) == 10:
                return date_time * 1000
            elif len(str(date_time)) == 13:
                return date_time
            elif date_time == 0:
                return date_time
            else:
                raise Exception(f"date_time: {date_time} len: {len(str(date_time))}")

        if not isinstance(date_time, datetime):
            return 0
        str_time = date_time.strftime('%Y-%m-%d %H:%M:%S')
        time_array = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
        time_stamp = int(time.mktime(time_array)) * 1000
        return time_stamp
    except Exception as e:
        logger.info(e)
        return 0


def datetime_to_long10(date_time: datetime) -> int:
    return int(datetime_to_long(date_time=date_time) / 1000)


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
        if 4 < len(date_str) < 8:
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


def long_to_datetime(time_stamp):
    """
    时间戳转 "%Y-%m-%d %H:%M:%S"
    Args:
        time_stamp: 时间戳

    Returns: str

    """
    time_stamp = int(time_stamp)
    if len(str(time_stamp)) == 13:
        time_stamp = math.floor(time_stamp / 1000)
    time_array = time.localtime(time_stamp)
    other_style_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    other_style_time = datetime.strptime(other_style_time, "%Y-%m-%d %H:%M:%S")
    return other_style_time


def read_txt(path, _encoding='utf-8'):
    file = open(path, 'r+', encoding=_encoding)
    lines = file.readlines()
    file.close()
    to_str = 'amp;'.join(lines)
    to_str = to_str.replace('\n', '').lstrip('\ufeff')
    lines = to_str.split('amp;')
    return lines


def write_txt(path, content, mod='a+'):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    file = open(path, mod, encoding='utf-8')
    file.write(content)
    file.close()


def dict_to_object(py_data, obj, obj_dict=None):
    # py_data = json.loads(json_data)
    if obj_dict is None:
        obj_dict = {}
    dic2class(py_data, obj, obj_dict)
    return obj


def dic2class(py_data, obj, obj_dict):
    for name in [name for name in dir(obj) if not name.startswith('_')]:
        if name not in py_data:
            value = getattr(obj, name)
            setattr(obj, name, value)
        else:
            value = getattr(obj, name)
            try:
                setattr(obj, name, set_value(name, value, py_data[name], obj_dict))
            except Exception as e:
                logger.info(e)


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
    except Exception as e:
        logger.info(e)
        return None


def str_to_datetime(str_time):
    try:
        if isinstance(str_time, datetime):
            return str_time
        str_time = str_time.replace('/', '-')
        return datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        logger.info(e)
        return datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')


def datetime_to_str(date_time, time_str='%Y-%m-%d %H:%M:%S'):
    try:
        return date_time.strftime(time_str)
    except Exception as e:
        logger.info(e)
        return ''


def timedelta_add_year(date_time, add_year):
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
    elif other_type(obj):
        obj = str(obj)
    return obj


def check_object(obj):
    if obj.__class__.__name__ != 'type' and obj.__class__.__name__ != 'module' and hasattr(obj, '__dict__'):
        return True
    else:
        return False


def other_type(obj):
    conditions = [datetime, date, int, str, float, list, bool, dict]
    if any(isinstance(obj, c) for c in conditions):
        return False
    else:
        return True


def base_change(n: int, base: int):
    """
    10进制转换为任意进制
    :param n:
    :param base:
    :return:
    """
    convert_string = "0123456789ABCDEF"
    if n < base:
        return convert_string[n]
    else:
        return base_change(n // base, base) + convert_string[n % base]


def base_change_after(n: int, base: int):
    if base == 0:
        raise Exception(f"base不允许等于{base}")

    if base == 1:
        return 0

    ret = base_change(n=n, base=base)
    after = ret[-1]
    if after == "F":
        return 15
    elif after == "E":
        return 14
    elif after == "D":
        return 13
    elif after == "C":
        return 12
    elif after == "B":
        return 11
    elif after == "A":
        return 10
    else:
        return int(after)


def gmt_date(created_at):
    try:
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(created_at, '%a %b %d %H:%M:%S %z %Y'))
        create_time = datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
        logger.info(f"gmt_date error:{e}")
        create_time = datetime.strptime('0001-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    return create_time


def clean_dir(directory_path: Path):
    if not directory_path.is_dir():
        raise Exception(f"{directory_path.resolve()}不是目录")
    pass


def clean_file(file_path: Path):
    if not file_path.is_file():
        raise Exception(f"{file_path.resolve()}不是文件")
    pass


def pickle_load(name: str) -> object:
    with open(name, 'rb') as f:
        obj = pickle.load(f)
    return obj


def pickle_dump(name: str, obj: object):
    with open(name, 'wb') as f:
        pickle.dump(obj, file=f)


def delete_dict_none(_dict: dict) -> dict:
    _list = list(_dict.keys()).copy()
    for key in _list:
        if _dict[key] == '':
            _dict.pop(key)
    return _dict


def read_text(file: str, mode: str = 'r', encoding: str = 'utf-8') -> [str, bytes]:
    with open(file, mode, encoding=encoding) as f:
        text = f.read()
    return text


def get_list(name: str) -> list:
    _str = read_text(name)
    if not _str:
        return []
    _list = json.loads(_str)
    return _list


def run_project(cmd: list, cwd: str = '.') -> int:
    return psutil.Popen([*cmd], cwd=cwd, creationflags=16).pid


def wait_pid_end(pid: int):
    while psutil.pid_exists(pid=pid):
        time.sleep(3)


def kill_pid(_pid):
    if _pid != 0:
        os.system(f'taskkill /F /PID {_pid}')


def git_clone(username: str, password: str, url: str, cwd: str = '..') -> int:
    _url = re.search(r'://(.*)', url).group(1)
    username = parse.quote(username)
    password = parse.quote(password)
    git_url = f'http://{username}:{password}@{_url}'
    cmd = ['git', 'clone', git_url]
    return run_project(cmd, cwd=cwd)


def git_pull(cwd: str):
    cmd = ['git', 'pull']
    return run_project(cmd, cwd=cwd)


if __name__ == '__main__':
    # print(get_md5('http://weibo.com/7117188820/Jqojz4yNu'))
    # psutil.Popen(
    #     ['git', 'clone', 'http://1358244533%40qq.com:1358244533@14.23.114.74:3000/wudinggao/PyWeiboCrawler.git'],
    #     creationflags=16)
    # run_project(cmd=['git',
    #                  'clone', 'http://1358244533%40qq.com:1358244533@14.23.114.74:3000/wudinggao/PyWeiboCrawler.git'])
    # time.sleep(10)
    # print(loads(Path('../docs/client_json.json')))
    # kill_pid(5)
    # kill_pid(22448)
    # print(get_now_datetime())
    print(gmt_date("Thu Nov 26 13:16:15 +0800 2020"))
    print(type(long_to_datetime("Thu Nov 26 13:16:15 +0800 2020")))
