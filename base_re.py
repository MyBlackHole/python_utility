#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          base_re
   Description:
   Author:             Black Hole
   date:               2020/11/25
-------------------------------------------------
   Change Activity:    2020/11/25:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import re


def is_chinese(_str: str) -> bool:
    """
    是否包含中文
    Args:
        _str: 判定字符串
    Input: "我"
    Returns: True
    Class: <class 'bool'>
    """
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    chinese = re.search(pattern, _str)
    if chinese:
        return True
    return False


def is_un_chinese(_str: str) -> bool:
    """
    是否包含非中文
    Args:
        _str: 判定字符串
    Input: "我"
    Returns: False
    Class: <class 'bool'>
    """
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    chinese = re.search(pattern, _str)
    if chinese:
        return True
    return False


def del_prefix(content):
    """
    清除@对象
    :param content: 文本
    :return: str
    """
    for i in range(10):
        content_len = len(content)
        content = re.sub('^//@(.*?) ?: ?', '', content)
        if len(content) >= content_len:
            break
    return content


if __name__ == '__main__':
    print(is_un_chinese("0"))
