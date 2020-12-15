#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          base_str
   Description:
   Author:             Black Hole
   date:               2020/11/25
-------------------------------------------------
   Change Activity:    2020/11/25:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import re
from typing import Callable
from urllib.parse import urljoin

from loguru import logger


def key_split(_list: list, base_sep: str = '+', sep_list: list = [',', '+', ' ', '＋']) -> list:
    """
    分割字符串列表
    Args:
        _list: 数据源
        base_sep: 默认切换字符
        sep_list: 需要切分的字符列表
    Input: ['广州人社局+周江波＋贪污']
    Returns: ['广州人社局', '周江波', '贪污']
    Class: <class 'list'>
    """
    _list_all = []
    for i, item in enumerate(_list):
        for sep in sep_list:
            item = item.replace(sep, base_sep)
        _list_all.extend(item.split(base_sep))
    return _list_all


def clear_source(content_source: str, url: str, old_content: str) -> str:
    """
    对content进行格式化，方便阅读
    Args:
        content_source: 待处理文本
        url: url
        old_content: 默认文本

    Returns:

    """
    try:
        if content_source:
            content_source = re.sub(r'[{}\[\]]', '', content_source)  # 清除{}[]符号
            content_source = re.sub('[.]', '#1', content_source)
            content_source = re.sub('[*]', '#2', content_source)
            content_source = re.sub('[?]', '#3', content_source)
            content_source = re.sub('[(]', '#4', content_source)
            content_source = re.sub('[)]', '#5', content_source)  # 替换有转义意义的字符，分别用不同值代替
            # 清楚script和style标签及里面的内容，前提需要将原文的换行符替换为空，并且将转义字符替换，才不会在替换过程报错
            clear_script = re.sub('<script.*?>.*?</script>|<style>.*?</style>', '', content_source.replace('\n', ''))
            p_contents = re.findall('<[pP].*?>.*?</[pP]>', clear_script)  # 寻找全部p标签
            texts = []
            for p in p_contents:  # 循环遍历，
                p_text = re.search('<[pP].*?>(.*?)</[pP]>', p).group(1).strip()  # 找到每个p标签里的内容，在前面添加四个空格作为新p，跟旧p替换
                new_p = re.sub(p_text, f'    {p_text}', p)
                texts.append([new_p, p])
            for new_p, old_p in texts:
                clear_script = re.sub(old_p, new_p, clear_script)  # 将旧p全部替换为新p
            sub_n = re.sub('<[pP].*?>|<br>', '\\n', clear_script)  # p标签和br标签替换为换行符
            sub_img = re.sub('<img', '%img', sub_n)  # 替换为%是为了防止下面的将全部<.*?>替换为空
            clear_tag = re.sub('<.*?>|&nbsp;', '', sub_img)
            content = re.sub('%img', '<img', clear_tag)  # 换回去
            content = re.sub('#1', '.', content)
            content = re.sub('#2', '*', content)
            content = re.sub('#3', '?', content)
            content = re.sub('#4', '(', content)
            content = re.sub('#5', ')', content)  # 换回原意
            src_list = re.findall('src="(.*?)"', content)
            my_list = [i for i in src_list if i != '']  # 清除列表有空字符串，防止下面替换过程中出现替换太多次的结果
            add_hrefs = []
            # 将相对路径替换为绝对路径
            for old_href in my_list:
                if not old_href.startswith('http'):
                    new_href = urljoin(url, old_href)
                    add_hrefs.append([new_href, old_href])
            for new_href, old_href in add_hrefs:
                content = re.sub(old_href, new_href, content)
            if content == '':  # 如果为空，则用原content
                content = old_content
        else:
            content = old_content
    except Exception as e:
        logger.info(f"error: {e}")
        content = old_content
    return content


def key_filter(item_list: list, key: str, func: Callable) -> list:
    """
    通过 key 过滤列表
    Args:
        item_list: 待过滤数据
        key: 关键字
        func: item 属性提取的回调方法

    Returns: List

    """
    new_item_list = item_list.copy()
    for item in item_list:
        if key is func(item):
            new_item_list.remove(item)
    return new_item_list


def keys_filter(item_list: list, key_list: list, func: Callable) -> list:
    """
    过滤包含 keys 的数据
    Args:
        item_list: 待过滤数据
        key_list: 关键字列表
        func: item 属性提取的回调方法

    Returns: List

    """
    for key in key_list:
        item_list = key_filter(item_list=item_list, key=key, func=func)
    return item_list


def key_and_filter(item_list: list, key: str, seq: str, func: Callable) -> list:
    """
    且关系过滤
    Args:
        item_list: 待过滤数据
        key: 关键字列表
        seq: 切分
        func: item 属性提取的回调方法

    Returns: List

    """
    new_item_list = item_list.copy()
    key_and_list = key.split(seq)
    for item in item_list:
        for key in key_and_list:
            if key not in func(item):
                item = None
                break
        if item:
            new_item_list.remove(item)
    return new_item_list


def keys_and_filter(item_list: list, key_list: list, seq: str, func: Callable) -> list:
    """
    过滤包含 keys 的数据
    Args:
        item_list: 待过滤数据
        key_list: 关键字列表
        seq: 切分
        func: item 属性提取的回调方法

    Returns: List

    """
    for key in key_list:
        item_list = key_and_filter(item_list=item_list, key=key, seq=seq, func=func)
    return item_list


if __name__ == '__main__':
    _key_list = ['广州人社局+周江波＋贪污']
    print(key_split(_key_list))
