#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          conf
   Description:
   Author:             Black Hole
   date:               2020/7/28
-------------------------------------------------
   Change Activity:    2020/7/28:
-------------------------------------------------
"""

__author__ = 'Black Hole'

from pathlib import Path

MYSQL_INFO = {
    'host': '127.0.0.1',
    'user': 'black',
    'password': '123456',
    'database': 'text',
    'port': 4396
}

# redis 连接配置表
REDIS_INFO_LIST = [{"host": "127.0.0.1", "port": 6379}]

# 使用的redis数据量
SELECT_COUNT = 16

# 程序根目录路径
BASE_PATH = Path(__file__).parent

# 文档存放路径
DOCS_PATH = BASE_PATH / 'docs'
print(DOCS_PATH)
