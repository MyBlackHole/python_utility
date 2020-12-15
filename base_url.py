#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          base_url
   Description:
   Author:             Black Hole
   date:               2020/12/14
-------------------------------------------------
   Change Activity:    2020/12/14:
-------------------------------------------------
"""

__author__ = 'Black Hole'


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
