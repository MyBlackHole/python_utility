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

import arrow
from loguru import logger


def dumps_file(path: Path, data: [list, dict, str]):
    """
    是否包含中文
    Args:
        path: 路径对象
        data: 路径对象
    Input: path:'meta_search.json' data: {1:1}
    Returns: None
    """
    with open(path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))


def loads_file(path: Path) -> [list, dict, str]:
    """
    是否包含中文
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


def read_after(file_name: str, offset: int = -50) -> str:
    """
    读取最后一行
    :param file_name: 文件名
    :param offset: -50  # 设置偏移量, 正往结束方向移动，负往开始方向移动。
    :return: str
    """
    with open(file_name, 'rb') as f:  # 打开文件
        # 在文本文件中，没有使用b模式选项打开的文件，只允许从文件头开始,只能seek(offset,0)
        while True:
            try:
                """
                file.seek(off, whence=0)：从文件中移动off个操作标记（文件指针），正往结束方向移动，负往开始方向移动。
                如果设定了whence参数，就以whence设定的起始位为准，0代表从头开始，1代表当前位置，2代表文件最末尾位置。 
                """
                f.seek(offset, 2)  # seek(offset, 2)表示文件指针：从文件末尾(2)开始向前50个字符(-50)
                lines = f.readlines()  # 读取文件指针范围内所有行
                if len(lines) >= 2:  # 判断是否最后至少有两行，这样保证了最后一行是完整的
                    last_line = lines[-1]  # 取最后一行
                    break
                # 如果off为50时得到的read_lines只有一行内容，那么不能保证最后一行是完整的
                # 所以off翻倍重新运行，直到read_lines不止一行
                offset *= 2
            except Exception as e:
                raise Exception(f' 确保文件行数超过 2 行 error:{e} ')
        return last_line.decode()


def del_file(path: Path, past_time: int, rule: str):
    """
    根据 rule 匹配文件删除
    Args:
        path: 目录路径
        past_time: 距今多少天
        rule: re 规则

    Returns: None

    """
    for item in path.rglob(rule):
        if arrow.now().shift(days=past_time).timestamp > int(item.stat().st_mtime):
            item.unlink()
            logger.info(f'{item.resolve()} 删除成功')
