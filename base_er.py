#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          base_error
   Description:
   Author:             Black Hole
   date:               2020/7/23
-------------------------------------------------
   Change Activity:    2020/7/23:
-------------------------------------------------
"""

__author__ = 'Black Hole'

from pymysql import ProgrammingError
from requests.exceptions import ReadTimeout, ConnectionError, RequestException
from retrying import RetryError

from .entity.results import Results


def exception(results: Results, error, info):
    if isinstance(error, ProgrammingError):
        info = f"{info} {error.args}"
        results.error = info
        raise Exception(results.dumps())
    elif isinstance(error, RetryError):
        info = f"{info} {error.args}"
        results.error = info
        raise Exception(results.dumps())
    elif isinstance(error, ReadTimeout):
        info = f'{info} Timeout'
        results.error = info
        raise Exception(results.dumps())
    elif isinstance(error, ConnectionError):
        info = f'{info} Connection error'
        results.error = info
        raise Exception(results.dumps())
    elif isinstance(error, RequestException):
        info = f'{info} Error'
        results.error = info
        raise Exception(results.dumps())
    else:
        info = f'{info} {error}'
        results.error = info
        raise Exception(results.dumps())
