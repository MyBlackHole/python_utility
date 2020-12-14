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
        results.info = info
        results.error = {error.args}
        raise Exception(results.json())
    elif isinstance(error, LogException):
        results.error = error.body
        results.status_code = error.status_code
        results.info = error.url
        return results
    elif isinstance(error, RetryError):
        results.info = info
        results.error = {error.args}
        return results
    elif isinstance(error, ReadTimeout):
        info = f'{info} Timeout'
        results.error = info
        raise Exception(results.json())
    elif isinstance(error, ConnectionError):
        info = f'{info} Connection error'
        results.error = info
        raise Exception(results.dict())
    elif isinstance(error, RequestException):
        info = f'{info} Error'
        results.error = info
        raise Exception(results.json())
    else:
        results.info = info
        results.error = {error.args}
        raise Exception(results.json())


class LogException(Exception):
    def __init__(self, url: str, status_code: int, body: str):
        self.url = url
        self.status_code = status_code
        self.body = body


class RException(Exception):
    def __init__(self, results: Results):
        self.results: results
