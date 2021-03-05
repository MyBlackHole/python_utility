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

from pydantic import BaseModel, validator
from requests.models import Response

resp_type = Union[Response, tuple, int, None]
error_type = Union[tuple, str, None]


class Results(BaseModel):
    # 状态
    # success: bool = False
    success: bool = False

    # 异常信息
    # error: error_type = None
    error: error_type = None

    # 状态码
    status_code: int = -1

    # 请求响应
    # resp: resp_type = None
    resp: resp_type = None

    # url等
    info: str = None

    class Config:
        arbitrary_types_allowed = True


if __name__ == '__main__':
    print(Results().json())
    pass
    # print(Results(success=True))
    # print(Results())
