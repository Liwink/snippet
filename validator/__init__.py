#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

字段验证器：用于验证输入的数据是否为预期的类型、格式等

注意：

- 所有验证器统一返回值为 bool 类型
    - True 验证通过
    - False 验证不通过

参考：

- https://github.com/django/django/blob/master/django/core/validators.py
"""

__author__ = 'Liwink'

import re
import datetime

from ..pylibs_settings import config
import i18n


def url_validator(value):
    """
    URL 验证

    ^ 匹配字符串开头
    $ 匹配字符串末尾
    \S 非空白字符 [^\s]
    + 匹配前一个字符一次或无限次
    """
    pattern = re.compile(r'^https?://\S+$')
    result = pattern.match(value)
    return bool(result)


def phone_validator(value):
    """
    手机号码验证
        - 支持国际号码
    大陆号码1开头      11位
    香港号码 [569]开头 8位
    澳门号码6开头      8位
    参考
        https://github.com/daviddrysdale/python-phonenumbers

    这里就可以看到动态配置的方便，可以根据环境对返回值、判断等做调整

    [] 字符集，对应可以是字符集中任意字符 [abc]==[a-c]，如需表示特殊字符如：^ - ]，可以在前面加上反斜杠
    | 左右表达式任意匹配，左边优先
    """
    if config.env in ['staging']:
        return re.compile(r"^1[0-9]{10}$|^[569][0-9]{7}$|6[0-9]{7}$").match(value) \
               or re.compile(r"^8888[0-9]{4,7}$").match(value)
    return re.compile(r"^1[0-9]{10}$|^[569][0-9]{7}$|6[0-9]{7}$").match(value)


def date_validator(value):
    """
    验证日期格式
        - 标准格式： YYYY-mm-dd
    :returns date or False

    这里不太一样，如果通过验证后，会换回格式化的值。 使用场景应该是 schema Use
    没有看懂下面注释
    >>> datetime.datetime.strptime('1020-10-01', "%Y-%m-%d")
    datetime.datetime(1020, 10, 1, 0, 0)
    """
    try:
        value = datetime.datetime.strptime(value, '%Y-%m-%d')
        # the datetime strftime() methods require year >= 1900
        return value if value.year >= 1900 else False
    except:
        return False


def name_validator(value):
    """
    允许中文、罗马字符、阿拉伯数字、空格（多空格处并为一个），不允许任何标点符号
    :return:  如果匹配则返回处理后的字符串,如果不匹配则返回False

    [\u4e00-\u9fa5] 对所有中文匹配

    pattern = re.compile("(\s+)")
    value = pattern.sub(lambda x: " ", value)
    """
    value = value.strip()
    if not isinstance(value, unicode):
        value = value.decode("utf-8")
    pattern = re.compile(u"^[\u4e00-\u9fa5A-Za-z0-9\s]+$")
    match = pattern.match(value)
    if match:
        # 多个空格合并为一个
        pattern = re.compile("(\s+)")
        value = pattern.sub(lambda x: " ", value)
        if i18n.is_all_chinese(value.replace(' ', '')):
            if 2 <= len(value) <= 6:
                return value
            return False
        elif i18n.is_chinese(value):
            print(value)
            if 2 <= len(value) <= 20:
                return value
        else:
            return False
    return False



