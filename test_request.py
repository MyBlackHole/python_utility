#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          text_request
   Description:
   Author:             Black Hole
   date:               2020/7/23
-------------------------------------------------
   Change Activity:    2020/7/23:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import pytest

from .bio_request import bio_get


@pytest.mark.parametrize('url', ['http://httpbin.org/', 'https://www.google.com/'])
def test_get(url):
    results, err = bio_get(url)
    if err:
        print(f"{err}")
    else:
        print(results.url)


if __name__ == '__main__':
    print(__file__)
    pytest.main(['-s', f'{__file__}'])
