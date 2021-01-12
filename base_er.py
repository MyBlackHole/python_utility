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

from loguru import logger
from requests.exceptions import ReadTimeout, ConnectionError, RequestException
from retrying import RetryError

from .entity.results import Results


def exception(results: Results, error, info):
    # if isinstance(error, ProgrammingError):
    #     results.info = info
    #     results.error = {error.args}
    #     logger.info(f"{results.json()}")
    #     return f"{results.json()}"
    if isinstance(error, LogException):
        results.error = error.body
        results.status_code = error.status_code
        results.info = error.url
        logger.info(f"{results.json()}")
        return f"{results.json()}"
    elif isinstance(error, RetryError):
        results.info = info
        results.error = {error.args}
        logger.info(f"{results.json()}")
        return f"{results.json()}"
    elif isinstance(error, ReadTimeout):
        info = f'{info} Timeout'
        results.error = info
        logger.info(f"{results.json()}")
        return f"{results.json()}"
    elif isinstance(error, ConnectionError):
        info = f'{info} Connection error'
        results.error = info
        logger.info(f"{results.json()}")
        return f"{results.json()}"
    elif isinstance(error, RequestException):
        info = f'{info} Error'
        results.error = info
        logger.info(f"{results.json()}")
        return f"{results.json()}"
    else:
        results.info = info
        results.error = {error.args}
        logger.info(f"{results.json()}")
        return f"{results.json()}"


class LogException(Exception):
    def __init__(self, url: str, status_code: int, body: str):
        self.url = url
        self.status_code = status_code
        self.body = body


class RException(Exception):
    def __init__(self, results: Results):
        self.results: results
