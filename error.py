#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          error
   Description:
   Author:             Black Hole
   date:               2020/7/23
-------------------------------------------------
   Change Activity:    2020/7/23:
-------------------------------------------------
"""

__author__ = 'Black Hole'

from requests.exceptions import ReadTimeout, ConnectionError, RequestException
from retrying import RetryError


def exception(results, error, url):
    if isinstance(error, RetryError):
        info = error.args
        results.error = info
        raise Exception(error.args)
    if isinstance(error, ReadTimeout):
        info = f'{url} Timeout'
        results.error = info
        raise Exception(info)
    if isinstance(error, ConnectionError):
        info = f'{url} Connection error'
        results.error = info
        raise Exception(info)
    if isinstance(error, RequestException):
        info = f'{url} Error'
        results.error = info
        raise Exception(info)
    if isinstance(error, Exception):
        info = f'{url} {error}'
        results.error = info
        raise Exception(info)
