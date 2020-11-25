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
    是否包含中文
    Args:
        _str: 判定字符串
    Input: "我"
    Returns: False
    Class: <class 'bool'>
    """
    return not is_chinese(_str=_str)


if __name__ == '__main__':
    print(is_un_chinese("0"))
