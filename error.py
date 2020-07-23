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
        results.error = error.args
        return
    if isinstance(error, ReadTimeout):
        results.error = f'{url} Timeout'
        return
    if isinstance(error, ConnectionError):
        results.error = f'{url} Connection error'
        return
    if isinstance(error, RequestException):
        results.error = f'{url} Error'
        return
    if isinstance(error, Exception):
        results.error = f'{url} {error}'
        return
