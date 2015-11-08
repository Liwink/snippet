#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Dylan'

import logging

import tornado.web
from pylibs.models import conn as m
from pylibs.constants import message_code
from pylibs.pubsub import publish


logger = logging.getLogger(__name__)


class HooksMixin(tornado.web.RequestHandler):
    """
    CRUD Hooks
        - post_hooks
        - update hooks
        - delete hooks

    """

    def pre_save_document(self, doc):
        """
        save动作：
            m.DocumentName.add
        :param doc:
        :return:
        """
        return True

    def post_add_documents(self, docs):
        """
        post add
        :param docs:
        :return:
        """
        pass

    def pre_update_document(self, criteria, doc):
        """
        update动作：
             m.DocumentName.update_by_id
             m.DocumentName.update_by_criteria
        :param criteria:
        :param doc:
        """
        return True

    def post_update_documents(self, docs):
        """
        post update
        :param docs:
        :return:
        """
        pass

    def pre_delete_document(self, criteria):
        """
        delete动作：
             m.DocumentName.remove_by_id
             m.DocumentName.remove_by
        :param criteria:
        :return:
        """
        return True

    def post_delete_documents(self, docs):
        """
        post delete
        :param docs:
        :return:
        """
        pass
