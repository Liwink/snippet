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
        self.taskmap = {}

    def new(self, target):
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask
        self.ready.put(newtask)

    def mainloop(self):
        while self.taskmap:
            task = self.ready.get()
            task.run()
            self.ready.put(task)


def foo():
    print("Part 1")
    yield
    print("Part 2")
    yield
