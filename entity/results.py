#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:   results
   Description: 请求、sql 执行结果返回实体
   Author:      Black Hole
   date:        2020/5/18
-------------------------------------------------
   Change Activity:
                2020/5/18:
-------------------------------------------------
"""

__author__ = 'Black Hole'

from typing import Union

from requests.models import Response

resp_type = Union[Response, tuple, int, None]
error_type = Union[tuple, str, None]


class Results(object):
    def __init__(self):
        # 状态
        self.success: bool = False

        # 异常信息
        self.error: error_type = None

        # 请求响应
        self.resp: resp_type = None
