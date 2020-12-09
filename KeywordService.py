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


# 12月2日
# def parse_md5(blog: Blog, task):
#     try:
#         md5_entity = MD5Entity()
#         if not str_is_none(blog.quoteID):
#             qid_md5 = get_md5(blog.quoteID)
#             md5_entity.qblogidMd5 = qid_md5
#             mc = re.findall('#[^#]+#', blog.quote)
#             for mtc in mc:
#                 top_md5 = get_md5(mtc)
#                 md5_entity.topicNameMD5.append((top_md5))
#             mc = re.findall('http://t.cn/[a-zA-Z0-9_]+', blog.quote)
#             for mtc in mc:
#                 qshorturl = ShortUrlEntity()
#                 shor_url_md5 = mtc
#                 if task.site == 1:
#                     try:
#                         if shor_url_md5 not in task.weibo_short:
#                             task.weibo_short.append(shor_url_md5)
#                         qshorturl.shortUrl = shor_url_md5
#                         blog.qshortUrlInfo.append((qshorturl))
#                     except Exception as e:
#                         logger.exception(e)
#         else:
#             md5_entity.qblogidMd5 = ''
#         m_coll = re.findall('#[^#]+#', blog.content)
#         for mtc in m_coll:
#             mtc_b = json.dumps(mtc)
#             mtc = json.loads(mtc_b)
#             top_md5 = get_md5(mtc)
#             md5_entity.topicNameMD5.append(top_md5)
#         m_coll = re.findall('http://t.cn/[a-zA-Z0-9_]+', blog.content)
#         for mtc in m_coll:
#             short_url = ShortUrlEntity()
#             shor_url_md5 = mtc
#             if task.site == 1:
#                 try:
#                     if shor_url_md5 not in task.weibo_short:
#                         task.weibo_short.append(shor_url_md5)
#                     short_url.shortUrl = shor_url_md5
#                     blog.shortUrlInfo.append((short_url))
#                 except Exception as e:
#                     logger.debug(f"error: {e}")
#             md5_entity.shortUrlMD5.append(shor_url_md5)
#         blog.md5s = md5_entity
#
#     except Exception as e:
#         logger.debug(f"error: {e}")


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
