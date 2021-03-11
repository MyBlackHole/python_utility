#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name:   queue_file
   Description:
   Author:      Black Hole
   date:        2020/6/5
-------------------------------------------------
   Change Activity:
                2020/6/5:
-------------------------------------------------
"""

__author__ = 'Black Hole'

from pathlib import Path
from queue import Queue
from threading import Thread


class QueueFile(object):
    """
    多线程队列写入文件
    """
    operate = None
    q = Queue()
    status = False

    def __new__(cls, *args, **kwargs):
        if not cls.operate:
            cls.operate = object.__new__(cls)
        return cls.operate

    def __init__(self):
        Thread(target=self.write).start()

    def put(self, text):
        self.q.put(text)

    def write(self):
        while True:
            if not self.q.qsize() > 0:
                if self.status:
                    break
                continue

            text = self.q.get()
            with open(Path('uid100.txt'), 'a', encoding='utf-8') as f:
                f.write(text + "\n")

# def put(qf, i):
#     qf.q.put(str(i))
#
#
# if __name__ == "__main__":
#     queue_file = QueueFile()
#     T = []
#     for i in range(100):
#         T.append(Thread(target=put, args=(queue_file, i)))
#
#     for t in T:
#         t.start()
#
#     for t in T:
#         t.join()
#     queue_file.status = True
