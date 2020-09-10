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
from retrying import retry, RetryError

from .entity.results import Results
from .base_er import exception


@retry(stop_max_attempt_number=3, stop_max_delay=400, wait_fixed=100)
def get_check(url: str, check_str: str):
    results = get(url=url)
    resp = results.resp
    if check_str not in resp.text:
        raise Exception(f"text 不包含{check_str}")
    return resp.text


@retry(stop_max_attempt_number=3, stop_max_delay=400, wait_fixed=100)
def get_check(url: str, check_str: str):
    results = get(url=url)
    resp = results.resp
    if check_str not in resp.text:
        raise Exception(f"text 不包含{check_str}")
    return resp.text


def post(url: str, **kwargs: dict) -> Results:
    """
    post 重试封装
    :param url: 链接
    :param kwargs:
        requests.post 一致
        stop_max_attempt_number: 总重试时间
        stop_max_delay: 重试次数
    :return: results 对象
    """
    results = Results()
    try:
        resp = Request().request("post", url, **kwargs)
        results.resp = resp
        results.success = True
    except Exception as e:
        exception(results=results, error=e, url=url)
    return results


def get(url: str, **kwargs: dict):
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
        exception(results=results, error=e, url=url)
    return results


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
            raise RetryError(f' url：{url} 响应码：{resp.status_code} ')
        return resp


if __name__ == "__main__":
    print(get('http://www.baidu.com'))
