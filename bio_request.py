#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:   request
   Description: 请求、发包模块
   Author:      Black Hole
   date:        2020/5/18
-------------------------------------------------
   Change Activity:
                2020/5/18:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import requests
from retrying import retry

from .base_er import exception, LogException
from .entity.results import Results


def bio_get_check(url: str, check_str: str):
    results, err_status = bio_get(url=url)
    resp = results.resp
    if check_str not in resp.text:
        raise Exception(f"text 不包含{check_str}")
    return resp.text


def bio_post(url: str, **kwargs: dict) -> [Results, bool]:
    """
    post 重试封装
    :param url: 链接
    :param kwargs:
        requests.post 一致
        stop_max_attempt_number: 总重试时间
        stop_max_delay: 重试次数
    :return: results 对象 bool
    """
    results = Results()
    try:
        resp = Request().request("post", url, **kwargs)
        results.resp = resp
        results.success = True
    except Exception as e:
        return exception(results=results, error=e, info=url), False
    return results, True


def bio_get(url: str, **kwargs: dict) -> [Results, bool]:
    """
    get 重试封装
    :param url: 链接
    :param kwargs:
        requests.get 一致
        stop_max_attempt_number: 总重试时间
        stop_max_delay: 重试次数
    :return: results 对象
    """
    results = Results()
    try:
        resp = Request().request("get", url=url, **kwargs)
        results.resp = resp
        results.success = True
    except Exception as e:
        return exception(results=results, error=e, info=url), False
    return results, True


class Request:
    stop_max_attempt_number = 3
    stop_max_delay = 6000
    wait_fixed = 2000

    def __init__(self, stop_max_attempt_number=stop_max_attempt_number, stop_max_delay=stop_max_delay):
        self.stop_max_attempt_number = stop_max_attempt_number
        self.stop_max_delay = stop_max_delay

    @retry(stop_max_attempt_number=stop_max_attempt_number, stop_max_delay=stop_max_delay, wait_fixed=wait_fixed)
    def request(self, method, url, **kwargs):
        # headers = {
        #     'Connection': 'close'
        # }
        resp = getattr(requests, method)(url=url, **kwargs)
        if not resp.status_code == 200:
            raise LogException(url=url, status_code=resp.status_code, body=resp.text)
        return resp


if __name__ == "__main__":
    print(bio_get('http://www.baidu.com'))
