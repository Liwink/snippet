#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Liwink'

import BaseHandler
import Mixin
import conn


class TestHandler(Mixin, BaseHandler):
    document = 'TestDocument'

    def get(self):
        result = self.getDocument()
        self.write(result)


##### Mixin
class TestMixin(BaseHandler):
    document = None

    def getDocument(self):
        conn[self.document].find_by_page_with_builtin_pagination(self.criteria)
        # 管爷这里写 self.criteria，给了客户端很多灵活性，和后台的特性极其温和。但是对于一般客户端，需求更为固定（不会有多种查询），拼接更复杂（admin 中的查询多是当前表的查询，或者基于关联表的查询）。


