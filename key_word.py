#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          KeywordService
   Description:
   Author:             Black Hole
   date:               2020/9/18
-------------------------------------------------
   Change Activity:    2020/9/18:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import re

import jieba
import jieba.analyse
from loguru import logger


def get_nick_name_by_index(text):
    names = ''
    try:
        mc = re.findall(r'@([\u4e00-\u9fa5\w\-]+)', text)
        for at_name in mc:
            names += at_name + ' '
        names = names.strip(' ')

    except Exception as e:
        logger.debug(f"error: {e}")

    return names


def jb_parse_keywords(count: int, text: str):
    return ' '.join(jieba.analyse.textrank(text, topK=count))
