#!/usr/bin/env python
# encoding: utf-8

class Observable:

    def __init__(self):
        self.__observers = []

    def register_observer(self, observe):
        self.__observers.append(observe)

    def notify_observers(self, *args, **kwargs):
        for observe in self.__observers:
            observe.notify(self, *args, **kwargs)

class Observer:

    def __init__(self, observable):
        observable.register_observer(self)

    def notify(self, observable, *args, **kwargs):
        print("Got", args, kwargs, "From", observable)


if __name__ == "__main__":
    subject = Observable()
    observer = Observer(subject)
    subject.notify_observers("test")
