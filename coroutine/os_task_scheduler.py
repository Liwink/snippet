#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import queue


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
        self.ready = queue.Queue()
        self.taskmap = {}

    def new(self, target):
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)

    def schedule(self, task):
        self.ready.put(task)

    def exit(self, task):
        print("Task {0} terminated.".format(task.target.__name__))
        del self.taskmap[task.tid]

    def mainloop(self):
        while self.taskmap:
            task = self.ready.get()
            try:
                result = task.run()
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)


def foo():
    for i in range(10):
        print("I'm foo")
        yield


def bar():
    for i in range(10):
        print("I'm bar")
        yield

if __name__ == "__main__":
    s = Scheduler()
    s.new(foo())
    s.new(bar())
    s.mainloop()

