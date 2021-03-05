#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:          base_aiohttp
   Description:
   Author:             Black Hole
   date:               2020/11/27
-------------------------------------------------
   Change Activity:    2020/11/27:
-------------------------------------------------
"""

__author__ = 'Black Hole'

import asyncio

import aiohttp


async def aio_get(url: str, **kwargs: dict) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, **kwargs) as response:
            assert response.status == 200
            return await response.read()


async def aio_post(url: str, **kwargs: dict) -> bytes:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, **kwargs) as response:
            assert response.status == 200
            return await response.read()


async def print_aio_get(url: str):
    html = await aio_get(url=url)
    print(html.decode())


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    task = asyncio.ensure_future(print_aio_get(url='http://www.baidu.com/'))
    resp = loop.run_until_complete(asyncio.wait([task]))
