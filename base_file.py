#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          base_file
   Description:
   Author:             Black Hole
   date:               2020/11/25
-------------------------------------------------
   Change Activity:    2020/11/25:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import json
from pathlib import Path
from typing import Union


def dumps_file(path: Path, data: Union[list, dict]):
    """
    Args:
        path: 路径对象
        data: 路径对象
    Input: path:'meta_search.json' data: {1:1}
    Returns: None
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))


def loads_file(path: Path) -> Union[list, dict]:
    """
    Args:
        path: 路径对象
    Input: 'meta_search.json'
    Returns: {1:1}
    Class: <class 'dict'>
    """
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
        if not text:
            return {}
        return json.loads(text)
