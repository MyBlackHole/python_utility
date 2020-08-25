#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          base_redis
   Description:
   Author:             Black Hole
   date:               2020/8/17
-------------------------------------------------
   Change Activity:    2020/8/17:
-------------------------------------------------
"""

__author__ = 'Black Hole'

from typing import List

import redis
from pydantic import BaseModel
from redis import ConnectionPool, Redis

from etc.conf import SELECT_COUNT, redis_info_list
from .base import base_change_after


class RedisSelect(BaseModel):
    host: str
    port: int
    select_list: List[ConnectionPool] = []
    select_count: int = SELECT_COUNT

    class Config:
        arbitrary_types_allowed = True

    def init(self):
        for index in range(self.select_count):
            pool = redis.ConnectionPool(host=self.host, port=self.port, db=index)
            self.select_list.append(pool)

    def get_conn(self, db: int = 0, *args, **kwargs) -> Redis:
        pool = self.select_list[base_change_after(db, self.select_count)]
        return Redis(connection_pool=pool, *args, **kwargs)


class RedisManage(BaseModel):
    instance_list: List[RedisSelect] = []
    instance_count: int = 0

    def init(self, info_list: List[dict]):
        for item in info_list:
            redis_select = RedisSelect(**item)
            redis_select.init()
            self.instance_list.append(redis_select)
        self.instance_count = len(self.instance_list)

    def get_conn(self, index: int = 0, db: int = 0, *args, **kwargs) -> Redis:
        redis_select = self.instance_list[base_change_after(index, self.instance_count)]
        return redis_select.get_conn(db=db, *args, **kwargs)


redis_manage = RedisManage()
redis_manage.init(info_list=redis_info_list)


def redis_conn(index: int = 0, db: int = 0) -> Redis:
    return redis_manage.get_conn(index=index, db=db)


def flush_db() -> str:
    for i in range(redis_manage.instance_count):
        for j in range(SELECT_COUNT):
            redis_manage.get_conn(index=i, db=j).flushdb()
    return "成功"


def db_size() -> dict:
    size = {}
    for i in range(redis_manage.instance_count):
        size[i] = {}
        for j in range(SELECT_COUNT):
            resp = redis_manage.get_conn(index=i, db=j).dbsize()
            if none_or_0(resp):
                continue
            size[i][j] = resp
    return size


def all_task_count() -> dict:
    size = {}
    for i in range(redis_manage.instance_count):
        size[i] = {}
        for j in range(SELECT_COUNT):
            resp = redis_manage.get_conn(index=i, db=j).llen('task')
            if none_or_0(resp):
                continue
            size[i][j] = resp
    return size


def current(func: str, select: dict, *args, **kwargs) -> dict:
    size = {}
    if not hasattr(redis_manage.get_conn(), func):
        return {"mes": f"没有{func}方法"}

    for i in range(redis_manage.instance_count):

        if select and not select.get(i):
            continue

        for j in range(SELECT_COUNT):
            if select and j not in select.get(i):
                continue

            try:
                if args == () and kwargs == {}:
                    resp = getattr(redis_manage.get_conn(index=i, db=j), func)()
                    resp_new = filter_none(resp)
                    if resp_new:
                        size[i] = {}
                        size[i][j] = resp_new
                    continue
                elif args != () and args[0]:
                    resp = getattr(redis_manage.get_conn(index=i, db=j), func)(*args)
                    resp_new = filter_none(resp)
                    if resp_new:
                        size[i] = {}
                        size[i][j] = resp_new
                    continue
                else:
                    resp = getattr(redis_manage.get_conn(index=i, db=j), func)(**kwargs)
                    resp_new = filter_none(resp)
                    if resp_new:
                        size[i] = {}
                        size[i][j] = resp_new
                    continue
            except Exception as e:
                return {"mes": f"{e}"}
    return size


def filter_none(resp: list):
    resp_new = []
    for item in resp:
        if item:
            resp_new.append(item)
    return resp_new


def none_or_0(resp):
    if not resp or resp == 0:
        return True


if __name__ == "__main__":
    print(db_size())
