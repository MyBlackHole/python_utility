#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          base_weibo
   Description:
   Author:             Black Hole
   date:               2020/11/26
-------------------------------------------------
   Change Activity:    2020/11/26:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import math

from loguru import logger

__ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def base62_encode(num, alphabet=__ALPHABET):
    """Encode a number in Base X

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def base62_decode(string, alphabet=__ALPHABET):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num


def bid_to_mid(bid):
    bid = str(bid)[::-1]
    if len(bid) % 4 == 0:
        size = len(bid) / 4
    else:
        size = len(bid) / 4 + 1
    size = math.floor(size)
    result = []
    for i in range(size):
        s = bid[i * 4: (i + 1) * 4][::-1]
        s = str(base62_decode(str(s)))
        s_len = len(s)
        if i < size - 1 and s_len < 7:
            s = (7 - s_len) * '0' + s
        result.append(s)
    result.reverse()
    return int(''.join(result))


def mid_to_bid(mid):
    mid = str(mid)[::-1]
    if len(mid) % 7 == 0:
        size = len(mid) / 7
    else:
        size = len(mid) / 7 + 1
    size = math.floor(size)
    result = []
    for i in range(size):
        s = mid[i * 7: (i + 1) * 7][::-1]
        s = base62_encode(int(s))
        s_len = len(s)
        if i < size - 1 and len(s) < 4:
            s = '0' * (4 - s_len) + s
        result.append(s)
    result.reverse()
    return ''.join(result)


def get_title(annotations):
    title = []
    try:
        for item in annotations:
            if isinstance(item, str):
                if 'title' == item:
                    if annotations['title'] is not None and annotations['title'] not in title:
                        title.append(annotations['title'])
                continue
            if item is None:
                continue
            for key in item:
                if 'title' == key:
                    if item[key] is not None and key not in title:
                        title.append(item[key])
                else:
                    info = item[key]
                    if isinstance(info, dict):
                        for key2 in info:
                            if 'title' == key2:
                                if info[key2] is not None and key2 not in title:
                                    title.append(info[key2])
    except Exception as e:
        logger.exception(f" error：{e} {annotations} ")

    return title


if __name__ == '__main__':
    print(bid_to_mid('JvG6TmV4c'))
