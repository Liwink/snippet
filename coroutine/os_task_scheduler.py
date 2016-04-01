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
                if isinstance(result, SystemCall):
                    # the environment information
                    result.task = task
                    result.sched = self
                    result.handle()
                    continue
            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)


class SystemCall:
    """
    - In a real operating system, traps are how application programs
    request the services of the operation system
    - In our code, the scheduler is the operating system and the yield
    statement is a trap
    - To request the service of the scheduler, tasks will use the yield
    statement with a value
    """

    def handle(self):
        pass


class GetTid(SystemCall):
    def handle(self):
        self.task.sendval = self.task.tid
        self.sched.schedule(self.task)


def foo():
    # yield, send
    mytid = yield GetTid()
    for i in range(10):
        print("I'm foo", mytid)
        yield


def bar():
    mytid = yield GetTid()
    for i in range(10):
        print("I'm bar", mytid)
        yield


if __name__ == "__main__":
    s = Scheduler()
    s.new(foo())
    s.new(bar())
    s.mainloop()
