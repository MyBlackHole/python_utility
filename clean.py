#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:   clean
   Description:
   Author:      Black Hole
   date:        2020/6/22
-------------------------------------------------
   Change Activity:
                2020/6/22:
-------------------------------------------------
"""

__author__ = 'Black Hole'

from pathlib import Path


def clean_dir(directory_path: Path):
    if not directory_path.is_dir():
        raise Exception(f"{directory_path.resolve()}不是目录")
    pass


def clean_file(file_path: Path):
    if not file_path.is_file():
        raise Exception(f"{file_path.resolve()}不是文件")
    pass
