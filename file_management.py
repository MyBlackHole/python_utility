#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          file_management
   Description:
   Author:             Black Hole
   date:               2020/8/5
-------------------------------------------------
   Change Activity:    2020/8/5:
-------------------------------------------------
"""

__author__ = 'Black Hole'

from pathlib import Path

import arrow
from loguru import logger


def del_file(path: Path, past_time: int, rule: str):
    """
    根据 rule 匹配文件删除
    Args:
        path: 目录路径
        past_time: 距今多少天
        rule: re 规则

    Returns:

    """
    for item in path.rglob(rule):
        if arrow.now().shift(days=past_time).timestamp > int(item.stat().st_mtime):
            item.unlink()
            logger.info(f'{item.resolve()} 删除成功')


if __name__ == "__main__":
    pass
    # del_file(config.http_path, -10, '*.txt')
