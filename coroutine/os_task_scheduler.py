#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import Queue


class Task:
    taskid = 0

    def __init__(self, target):
        Task.taskid += 1
        self.tid = Task.taskid
        self.target = target
        self.sendval = None

    def run(self):
        return self.target.send(self.sendval)


class Scheduler:
    def __init__(self):
        self.ready = Queue()

    def new(self, task):
        pass

    def mainloop(self):
        while True:
            task = self.ready.get()
            task.run()
            self.ready.put(task)


def foo():
    print("Part 1")
    yield
    print("Part 2")
    yield
