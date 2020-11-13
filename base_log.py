#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:   base_log
   Description: 默认日记
   Author:      Black Hole
   date:        2020/5/27
-------------------------------------------------
   Change Activity:
                2020/5/27:
-------------------------------------------------
"""

__author__ = 'Black Hole'

from loguru import logger
from notifiers.logging import NotificationHandler

from .etc.conf import BaseConfig


class Log(object):
    def __init__(self, name=None):
        """
        初始化
        """
        init(name=name)


def init(name: str):
    log_path = BaseConfig.DOCS_PATH / "log"

    # 是否开启回溯
    backtrace = True

    rotation = "50 MB"

    def info_only(record):
        return record["level"].name == "INFO"

    logger.add(log_path / "info_log.log", backtrace=backtrace, filter=info_only, rotation=rotation, encoding="utf-8",
               enqueue=True,
               retention="14 days")

    def warning_only(record):
        return record["level"].name == "WARNING"

    logger.add(log_path / "warning_log.log", backtrace=backtrace, filter=warning_only, rotation=rotation,
               encoding="utf-8",
               enqueue=True,
               retention="14 days")

    def debug_only(record):
        return record["level"].name == "DEBUG"

    logger.add(log_path / "debug_log.log", backtrace=backtrace, filter=debug_only, rotation=rotation, encoding="utf-8",
               enqueue=True,
               retention="14 days")

    def error_only(record):
        return record["level"].name == "ERROR"

    logger.add(log_path / "error_log.log", backtrace=backtrace, filter=error_only, rotation=rotation, encoding="utf-8",
               enqueue=True,
               retention="14 days")

    # params = {
    #     "host": "smtp.qq.com",
    #     "port": 465,
    #     "username": "1358244533@qq.com",
    #     "from": "1358244533@qq.com",
    #     "password": "wettvkqaipkdfgdi",
    #     "to": ['myisblackhole@163.com'],
    #     "subject": name,
    #     "ssl": True
    # }

    # handler = NotificationHandler("email", defaults=params)
    # logger.add(handler, filter=error_only)


if __name__ == '__main__':
    # # 测试用
    # notifier = notifiers.get_notifier("email")
    # notifier.notify(message="The application is running!", **params)
    logger.info("中文test")
    logger.debug("中文test")
    logger.warning("中文test")
    logger.error("中文test")
    logger.info('If you are using Python {}, prefer {feature} of course!', 3.6, feature='f-strings')
    n1 = "cool"
    n2 = [1, 2, 3]
    logger.info(f'If you are using Python {n1}, prefer {n2} of course!')
