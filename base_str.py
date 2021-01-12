#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          base_str
   Description:
   Author:             Black Hole
   date:               2020/11/25
-------------------------------------------------
   Change Activity:    2020/11/25:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import re
from typing import Callable
from urllib.parse import urljoin

from loguru import logger


def key_split(_list: list, base_sep: str = '+', sep_list: list = [',', '+', ' ', '＋']) -> list:
    """
    分割字符串列表
    Args:
        _list: 数据源
        base_sep: 默认切换字符
        sep_list: 需要切分的字符列表
    Input: ['广州人社局+周江波＋贪污']
    Returns: ['广州人社局', '周江波', '贪污']
    Class: <class 'list'>
    """
    _list_all = []
    for i, item in enumerate(_list):
        for sep in sep_list:
            item = item.replace(sep, base_sep)
        _list_all.extend(item.split(base_sep))
    return _list_all



def key_filter(item_list: list, key: str, func: Callable) -> list:
    """
    通过 key 过滤列表
    Args:
        item_list: 待过滤数据
        key: 关键字
        func: item 属性提取的回调方法

    Returns: List

    """
    new_item_list = item_list.copy()
    for item in item_list:
        if key is func(item):
            new_item_list.remove(item)
    return new_item_list


def keys_filter(item_list: list, key_list: list, func: Callable) -> list:
    """
    过滤包含 keys 的数据
    Args:
        item_list: 待过滤数据
        key_list: 关键字列表
        func: item 属性提取的回调方法

    Returns: List

    """
    for key in key_list:
        item_list = key_filter(item_list=item_list, key=key, func=func)
    return item_list


def key_and_filter(item_list: list, key: str, seq: str, func: Callable) -> list:
    """
    且关系过滤
    Args:
        item_list: 待过滤数据
        key: 关键字列表
        seq: 切分
        func: item 属性提取的回调方法

    Returns: List

    """
    new_item_list = item_list.copy()
    key_and_list = key.split(seq)
    for item in item_list:
        for key in key_and_list:
            if key not in func(item):
                item = None
                break
        if item:
            new_item_list.remove(item)
    return new_item_list


def keys_and_filter(item_list: list, key_list: list, seq: str, func: Callable) -> list:
    """
    过滤包含 keys 的数据
    Args:
        item_list: 待过滤数据
        key_list: 关键字列表
        seq: 切分
        func: item 属性提取的回调方法

    Returns: List

    """
    for key in key_list:
        item_list = key_and_filter(item_list=item_list, key=key, seq=seq, func=func)
    return item_list


if __name__ == '__main__':
    _key_list = ['广州人社局+周江波＋贪污']
    print(key_split(_key_list))
