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

from typing import Union

import cattr
from attr import attrs, attrib
from requests.models import Response

resp_type = Union[Response, tuple, int, None]
error_type = Union[tuple, str, None]


@attrs
class Results(object):
    # 状态
    # success: bool = False
    success = attrib(type=bool, default=False)

    # 异常信息
    # error: error_type = None
    error = attrib(type=error_type, default=None)

    # 请求响应
    # resp: resp_type = None
    resp = attrib(type=resp_type, default=None)

    def dumps(self):
        return cattr.unstructure(self)

    # def loads(self, _dict):
    #     return cattr.structure(_dict, self.__class__)


if __name__ == '__main__':
    # print(Results(success=True))
    _dict = cattr.unstructure(Results())
    # print(Results())
    print(Results(**_dict))
