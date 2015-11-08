#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Descusr'


def is_chinese(value):
    """
    是否为中文。
    :param value:
    :return:
    """
    if not value:
        return
    for uchar in value:
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
    return False


def is_all_chinese(value):
    """
    是否全部为中文。
    :param value:
    :return:
    """
    if not value:
        return False
    for uchar in value:
        if not (uchar >= u'\u4e00' and uchar <= u'\u9fa5'):
            return False
    return True
