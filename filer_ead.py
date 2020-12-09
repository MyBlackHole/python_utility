#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:   file_read
   Description:
   Author:      Black Hole
   date:        2020/6/28
-------------------------------------------------
   Change Activity:
                2020/6/28:
-------------------------------------------------
"""

__author__ = 'Black Hole'


def read_after(file_name, offset=-50):
    """
    返回文件最后一行
    f_name: 文件名
    offset: -50  # 设置偏移量, 正往结束方向移动，负往开始方向移动。
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
