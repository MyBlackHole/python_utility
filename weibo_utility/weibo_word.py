#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          weibo_word
   Description:
   Author:             Black Hole
   date:               2020/11/30
-------------------------------------------------
   Change Activity:    2020/11/30:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import math
import re

from loguru import logger

from utility.base import str_is_none


def word_count(text):
    text = text.strip()
    text = re.sub('\r\n', '\n', text)
    text_len = 0
    if len(text) > 0:
        _min = 41
        _max = 140
        url_len = 20
        n = text
        r = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
        total = 0
        for m in range(len(r)):
            url = r[m]
            byte_len = len(url) + len(re.findall('[^\x00-\x80]', url))
            if len(re.findall(r'^(http://t.cn)', url)) > 0:
                continue
            elif len(re.findall(r'^(http:\/\/)+(weibo.com|weibo.cn)', url)) > 0:
                total += byte_len if byte_len <= _min else (
                    url_len if byte_len <= _max else (byte_len - _max + url_len))
            else:
                total += url_len if byte_len <= _max else (byte_len - _max + url_len)
            n = n.replace(url, '')
        text_len = math.ceil((total + len(n) + len(re.findall('[^\x00-\x80]', n))) / 2.0)
    return text_len


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


def Layer(count):
    """
    根据粉丝数，划分博主等级
    :param count:
    :return:
    """
    try:
        if count < 3000:
            return 0

        if 3000 <= count < 10000:
            return 1

        if 10000 <= count < 50000:
            return 2

        if 50000 <= count < 100000:
            return 3

        if 100000 <= count < 300000:
            return 4

        if 300000 <= count < 500000:
            return 5

        if 500000 <= count < 1000000:
            return 6

        if 1000000 <= count < 3000000:
            return 7

        if 3000000 <= count < 5000000:
            return 8

        if 5000000 <= count < 10000000:
            return 9

        if count >= 10000000:
            return 10
    except Exception as e:
        logger.exception(e)
    return 0


def get_weibo_type(blog):
    """
    获取微博类型 1：原创 2：转发 3：评论 4：纯文本 5：图片微博 6：短链微博
    :param blog:
    :return:
    """
    weibo_type = []
    if str_is_none(blog.quoteAuthor):
        weibo_type.append('1')
    else:
        weibo_type.append('2')
    if blog.imgCounts > 0 or blog.qimgCounts > 0:
        weibo_type.append('5')
    if len(blog.videoUrl) > 0 or len(blog.shortUrlInfo) > 0 or len(blog.qshortUrlInfo) > 0:
        weibo_type.append('6')
    if '5' not in weibo_type and '6' not in weibo_type:
        weibo_type.append('4')

    weibo_type.sort()
    return ' '.join(weibo_type)
