#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 2020/12/13 22:40
@Author  : lex(luohai2233@163.com)
"""
import datetime

from . import db
from ..config.config import Cfg


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    def to_dict(self, filter=None):
        res_dict = {}
        if filter is None:
            filter = self.fields
        for key in filter:
            res_dict[key] = getattr(self, key)
                
        return res_dict


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

    