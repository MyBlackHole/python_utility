#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          base_url
   Description:
   Author:             Black Hole
   date:               2020/11/27
-------------------------------------------------
   Change Activity:    2020/11/27:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import re


def index_of_str(s1, s2, start_index=0):
    new_s1 = s1[start_index:]
    n1 = len(new_s1)
    n2 = len(s2)
    for i in range(n1 - n2 + 1):
        if new_s1[i:i + n2] == s2:
            return i + start_index
    else:
        return -1


def last_index(s1, s2):
    new_s1 = s1[::-1]
    new_s2 = s2[::-1]
    n1 = len(s1)
    n2 = len(s2)
    for i in range(n1 - n2 + 1):
        if new_s1[i:i + n2] == new_s2:
            return i
    else:
        return -1


def _clean_url(url):
    start = index_of_str(url, '//')
    length = -1
    if start > -1:
        length = index_of_str(url, '/', start + 2) - start - 2
        if length > -1:
            url = url[start + 2:start + 2 + length]
        else:
            url = url[start + 2:]
    else:
        start = index_of_str(url, '/')
        if start > -1:
            url = url[0:start]
    start = last_index(url, ':')
    if start > -1:
        url = url[0:start]
    return url


def _is_ip_add(url):
    url = _clean_url(url)
    if url == re.search(r"(\d{1,3}\.){3}\d{1,3}", url):
        if re.search(r"(\d{1,3}\.){3}\d{1,3}", url) is not None:
            ips = url.split('.')
            if len(ips) == 4 or len(ips) == 6:
                if int(ips[0]) < 256 and int(ips[1]) < 256 and int(ips[2]) < 256 and int(ips[3]) < 256:
                    return True
                else:
                    return False
    return False
