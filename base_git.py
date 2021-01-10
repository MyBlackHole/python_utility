#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

""" 
------------------------------------------------- 
   File Name:   base_git 
   Description: 
   Author:      Black Hole 
   date:        2020/12/23 

------------------------------------------------- 
   Change Activity: 
                2020/12/23: 
------------------------------------------------- 
"""

__author__ = 'Black Hole'

import re
from urllib import parse

from utility.base import run_project


def git_clone(username: str, password: str, url: str, cwd: str = '..') -> int:
    """
    project clone
    Args:
        username: user name
        password: user pwd
        url: git project url
        cwd: save path

    Returns: int

    """
    _url = re.search(r'://(.*)', url).group(1)
    username = parse.quote(username)
    password = parse.quote(password)
    git_url = f'http://{username}:{password}@{_url}'
    cmd = ['git', 'clone', git_url]
    return run_project(cmd, cwd=cwd)


def git_pull(cwd: str):
    cmd = ['git', 'pull']
    return run_project(cmd, cwd=cwd)
