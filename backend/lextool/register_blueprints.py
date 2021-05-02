#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 2020/12/13 20:32
@Author  : lex(luohai2233@163.com)
@File    : register_blueprints.py
@Software: PyCharm
"""
from backend.lextool.auth import identity
from backend.lextool.views.poem import PoemView
from backend.lextool.views.dwz import DwzView
from backend.lextool.views.user import UserView
from backend.lextool.views.enwords import WordsView
from backend.lextool.views.admin import AdminView
from backend.lextool.views.comment import CommentView
from backend.lextool.views.sci import SciTestView


def register_blueprints(app):
    app.register_blueprint(identity.identity, url_prefix='/auth')
    app.register_blueprint(PoemView.poem, url_prefix='/poem')
    app.register_blueprint(UserView.user, url_prefix='/user')
    app.register_blueprint(DwzView.dwz, url_prefix='/dwz')
    app.register_blueprint(WordsView.words, url_prefix='/words')
    app.register_blueprint(AdminView.admin, url_prefix='/admin')
    app.register_blueprint(CommentView.comment, url_prefix='/comment')
    app.register_blueprint(SciTestView.sci, url_prefix='/sci')
