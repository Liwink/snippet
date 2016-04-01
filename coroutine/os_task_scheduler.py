#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'


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
    task_list = []

    def new(self, task):
        pass

    def process(self):
        while True:
            task = Scheduler.task_list.pop()
            task.run()
            Scheduler.task_list.append(task)

def foo():
    print("Part 1")
    yield
    print("Part 2")
    yield


