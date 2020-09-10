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

from .base import base_change_after
from .etc.conf import CONFIG


class RedisSelect(BaseModel):
    host: str
    port: int
    select_list: List[ConnectionPool] = []
    select_count: int = CONFIG.SELECT_COUNT

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
redis_manage.init(info_list=CONFIG.REDIS_INFO_LIST)


def redis_conn(index: int = 0, db: int = 0) -> Redis:
    return redis_manage.get_conn(index=index, db=db)


if __name__ == "__main__":
    print(redis_conn())
