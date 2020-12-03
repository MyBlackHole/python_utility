#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          weibo_url
   Description:
   Author:             Black Hole
   date:               2020/11/30
-------------------------------------------------
   Change Activity:    2020/11/30:
-------------------------------------------------
"""

__author__ = 'Black Hole'

from etc.weibo_config import Config
from utility.base import str_is_none
from utility.base_url import _clean_url, _is_ip_add


def get_domain(url):
    try:
        if str_is_none(url):
            return ''
        url = _clean_url(url)
        if _is_ip_add(url):
            return url
        urls = url.split('.')
        head_url = ''
        for i in range(1, len(urls)):
            str_foot = urls[len(urls) - i].upper()
            if str_foot in Config.DOMAIN_KEYS:
                continue
            head_url = ''
            for j in range(1, i + 1):
                if urls[len(urls) - j].upper() == 'WWW':
                    break
                head_url = '.' + urls[len(urls) - j] + head_url

            return head_url[1:]
        return ''
    except:
        return ''
