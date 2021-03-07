#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 2020/12/13 22:40
@Author  : lex(luohai2233@163.com)
"""
import datetime

from . import db
from ..config.config import Cfg
from ..common.exceptions import FilterInvaild


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    def to_dict(self, filters=None, lst=False):
        res_dict = {}
        filters = self._validate_filters(filters)
        for key in filters:
            res_dict[key] = getattr(self, key)
                
        return res_dict
    
    def _validate_filters(self, filters):
        if filters is None:
            return self.fields
        filters = filters if isinstance(filters, list) else [filters]
        for filter in filters:
            if filter not in self.fields:
                raise FilterInvaild(filters)
        return filters


class ModelWithCreateAt(Base):
    __abstract__ = True
    create_at = db.Column(db.DateTime, default=datetime.datetime.now)


class PoetMixin(object):
    @classmethod
    def search_poet(cls, keyword, page):
        items = cls.query.filter(
            cls.poet.like("%%{}%%".format(keyword)) if keyword is not None else "") \
            .paginate(page=page, per_page=Cfg.TOOLS.pagination, error_out=False).items
        return [item.poet for item in items]

    @classmethod
    def search_keyword_total(cls, keyword):
        total = len(cls.query.filter(
            cls.poet.like("%%{}%%".format(keyword)) if keyword is not None else "").all())
        return total


class Like(Base):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    i_like = db.Column(db.Integer)
    uid = db.Column(db.String(8), index=True)
