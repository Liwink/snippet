#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Dylan'

import logging
import tornado.web
from bson import ObjectId
from pylibs import decorators
from pylibs.models import conn as m
from . import HooksMixin
from .publisher import PublisherMixin
import validators

logger = logging.getLogger(__name__)


class ResourceMixin(HooksMixin, PublisherMixin, tornado.web.RequestHandler):
    """
    ResourceMixin
        - get_document
        - update_document
        - delete_document
        - GET/PUT/DELETE verbs

    """
    document = None
    parent_document = None
    relation_document = None
    relation_document_id_field = 'relation_id'
    relation_field = None

    def get_document(self, _id):
        """
        获取单个文档
        :param _id:
        :return:
        """
        # 可以通过配置 self.criteria ，动态设置查询条件
        criteria = self.get_criteria or {}
        criteria.update({
            '_id': _id,
        })
        result = m[self.document].find_first_one_by(criteria,
                                                    include_fields=self.include_fields,
                                                    **self.ref_include_fields_kwargs)
        return result

    def update_document(self, _id, doc):
        """
        更新单个资源
        :param _id:
        :param doc:
        :return:
        """
        filtered_doc = self.filter_doc(doc,
                                       include_fields=self.updatable_fields,
                                       )
        criteria = self.put_criteria or {}
        criteria.update({
            '_id': _id,
        })
        if not self.pre_update_document(criteria, filtered_doc):
            return
        result = m[self.document].update_by_criteria(criteria, filtered_doc)
        if result:
            result = result.to_dict_with_ref_docs(include_fields=self.include_fields,
                                                  **self.ref_include_fields_kwargs)
        return result

    def delete_document(self, _id, doc=None):
        """
        删除单个document
        :param _id:
        :param doc:
        :return:
        """
        criteria = self.delete_criteria or {}
        criteria.update({
            '_id': _id,
        })
        if not self.pre_delete_document(criteria):
            return
        deleted_docs = self._delete_documents(self.document, criteria)
        return deleted_docs[0] if deleted_docs else None

    def get_documents(self):
        """
        获取资源列表
        :return:
        """
        result = m[self.document].find_by_page_with_builtin_pagination(self.criteria,
                                                                       last_id=self.last_id,
                                                                       limit=self.limit,
                                                                       sort=self.sort,
                                                                       include_fields=self.include_fields,
                                                                       **self.ref_include_fields_kwargs
                                                                       )
        return result

    def add_documents(self, docs):
        """
        批量新增资源
        :param docs:
        :return:
        """
        result = []
        for doc in docs:
            filtered_doc = self.filter_doc(doc, include_fields=self.addable_fields)
            if not self.pre_save_document(filtered_doc):
                continue
            added = m[self.document].add(filtered_doc)
            if added:
                added = added.to_dict()
            result.append(added)
        return result

    def update_documents(self, docs):
        """
        批量更新资源
        :param docs:
        """
        result = []
        criteria = self.put_criteria or {}
        for doc in docs:
            criteria['_id'] = doc.pop('id')
            filtered_doc = self.filter_doc(doc, include_fields=self.updatable_fields)
            if not self.pre_update_document(criteria, filtered_doc):
                continue
            updated = m[self.document].update_by_criteria(criteria, filtered_doc)
            result.append(updated)
        return result

    def delete_documents(self, docs):
        """
        批量删除资源
        :param docs:
        """
        result = []
        criteria = self.delete_criteria or {}
        for doc in docs:
            criteria.update({
                '_id': doc.get('id'),
            })
            if not self.pre_delete_document(criteria):
                continue
            deleted_docs = self._delete_documents(self.document, criteria)
            result.extend(deleted_docs)
        return result

    def get_relation_documents(self, _id):
        """
        获取关系文档
        :param _id:
        :return:
        """
        criteria = self.criteria or {}
        criteria.update({self.relation_field: _id})
        result = m[self.document].find_by_page_with_builtin_pagination(criteria,
                                                                       last_id=self.last_id,
                                                                       limit=self.limit,
                                                                       sort=self.sort,
                                                                       include_fields=self.include_fields,
                                                                       **self.ref_include_fields_kwargs
                                                                       )
        return result

    def add_relation_documents(self, _id, docs):
        """
        增加关系文档
        :param _id:
        :param docs:
        :return:
        """
        result = []
        for doc in docs:
            filtered_doc = self.filter_doc(doc, include_fields=self.post_include_fields)
            filtered_doc.update({
                self.relation_field: _id,
            })
            if not self.pre_save_document(filtered_doc):
                continue
            added = m[self.document].add(filtered_doc)
            if added:
                added['id'] = added.pop('_id')
                added['relation_id'] = added.get('id')
                result.append(added)
        return result

    def update_relation_documents(self, _id, docs, criteria=None):
        """
        更新关系文档
                    - 仅更新两者之间的关系
                    - 不更新关联/引用的文档
        :param docs:
        :param criteria:
        :return:
        """
        result = []
        criteria = criteria or {}
        for doc in docs:
            filtered_doc = self.filter_doc(doc, include_fields=self.put_include_fields)
            criteria.update({
                '_id': doc[self.relation_document_id_field],
                self.relation_field: _id,
            })
            if not self.pre_update_document(criteria, filtered_doc):
                continue
            updated = m[self.document].update_by_criteria(criteria, filtered_doc)
            if updated:
                updated.update({
                    'relation_id': updated.get('_id'),
                    'id': updated.pop('_id', None),
                })
                result.append(updated)
        return result

    def delete_relation_documents(self, _id, docs, criteria=None):
        """
        删除关系文档
                    - 仅删除两者之间的关系
                    - 不删除关联/引用的文档
        :param _id:
        :param docs:
        :param criteria:
        :return:
        """
        result = []
        criteria = criteria or {}
        for doc in docs:
            criteria.update({
                '_id': doc.get(self.relation_document_id_field),
            })
            if not self.pre_delete_document(criteria):
                continue
            deleted_docs = self._delete_documents(self.relation_document, criteria)
            result.extend(deleted_docs)
        return result

    def _delete_documents(self, document, criteria, include_documents=None):
        """
        删除记录
        :param document:
        :param criteria:
        :return:
        """
        func = getattr(self, '_delete_{d}'.format(d=document), None)
        if func and callable(func):
            return func(document, criteria, include_documents)
        return self._do_delete_documents(document, criteria, include_documents)

    def _do_delete_documents(self, document, criteria, include_documents=None):
        """
        删除文档
        :param document:
        :param criteria:
        :param include_documents:
        :return:
        """
        docs = m[document].remove_by(criteria, user_id=self.user_id) or []
        msg = 'Deleting {count} {document} with {criteria} by {user_id}'.format(count=len(docs), document=document,
                                                                                criteria=criteria,
                                                                                user_id=self.user_id
                                                                                )

        logging.info(msg)
        return docs

    def _delete_documents_and_related_resource(self, document, criteria, include_documents=None):
        """
        删除文档以及级联的资源
            - 注意操作的严重性
        :param document:
        :param criteria:
        :return:
        """
        result = []
        entity_id = '{e}_id'.format(e=self.entity)
        for doc in m[document].find(criteria):
            docs = self._delete_related_documents(doc.get('_id'),
                                                  (entity_id, 'object_id', 'delegation_id'),
                                                  include_documents)
            result.extend(docs)
            docs = self._do_delete_documents(document, criteria, include_documents)
            result.extend(docs)
        return result

    def _delete_related_documents(self, _id, relation_fields, include_documents=None):
        """
        删除关联的资源
            - 注意操作的严重性
        :param _id:
        :param relation_fields:
        :return:
        """
        result = []
        for document, obj in m._registered_documents.iteritems():
            for field in set(obj.structure.keys()).intersection(set(relation_fields)):
                criteria = {
                    field: ObjectId(_id),
                }
                docs = self._do_delete_documents(document, criteria, include_documents)
                result.extend(docs)
        return result

    def _is_document_referenced(self, _id, relation_fields):
        """
        document是否被其他资源使用
        :param _id:
        :param relation_fields:
        :return:
        """
        for document, obj in m._registered_documents.iteritems():
            for field in set(obj.structure.keys()).intersection(set(relation_fields)):
                criteria = {
                    field: ObjectId(_id),
                }
                if m[document].find_one(criteria):
                    return True
        return False
