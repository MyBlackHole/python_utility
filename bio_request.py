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

from typing import Tuple, Union
import requests
from requests.models import Response
from retrying import retry


def bio_get_check(url: str, check_str: str) -> Tuple[Union[str, None], Union[str, None]]:
    results, err = bio_get(url=url)
    if check_str not in results.text or err:
        return None, f"text 不包含{check_str} or err={err}"
    return results.text, None


def bio_post(url: str, **kwargs: dict) -> Tuple[Union[Response, None], Union[str, None]]:
    """
    post 重试封装
    :param url: 链接
    :param kwargs:
        requests.post 一致
        stop_max_attempt_number: 总重试时间
        stop_max_delay: 重试次数
    :return: Response, None
    """
    try:
        resp, err = Request().request("post", url, **kwargs)
        return resp, err
    except Exception as e:
        return None, str(e)


def bio_get(url: str, **kwargs: dict) -> Tuple[Union[Response, None], Union[str, None]]:
    """
    get 重试封装
    :param url: 链接
    :param kwargs:
        requests.get 一致
        stop_max_attempt_number: 总重试时间
        stop_max_delay: 重试次数
    :return: results 对象
    """
    try:
        resp, err = Request().request("get", url=url, **kwargs)
        return resp, err
    except Exception as e:
        return None, str(e)


class Request:
    stop_max_attempt_number = 3
    stop_max_delay = 6000
    wait_fixed = 2000

    def __init__(self, stop_max_attempt_number=stop_max_attempt_number, stop_max_delay=stop_max_delay):
        self.stop_max_attempt_number = stop_max_attempt_number
        self.stop_max_delay = stop_max_delay

    @retry(stop_max_attempt_number=stop_max_attempt_number, stop_max_delay=stop_max_delay, wait_fixed=wait_fixed)
    def request(self, method, url, **kwargs) -> Tuple[Union[Response, None], Union[str, None]]:
        # headers = {
        #     'Connection': 'close'
        # }
        resp = getattr(requests, method)(url=url, **kwargs)
        if not resp.status_code == 200:
            return None, str(resp.status_code)
        return resp, None


if __name__ == "__main__":
    print(bio_get('http://www.baidu.com'))
