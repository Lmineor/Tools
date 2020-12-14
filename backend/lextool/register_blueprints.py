#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 2020/12/13 20:32
@Author  : lex(luohai2233@163.com)
@File    : register_blueprints.py
@Software: PyCharm
"""
from .auth import identity
from .views.poem import PoemView
from .views.dwz import DwzView
from .views.user import UserView
from .views.enwords import WordsView
from .views.admin import AdminView
from .views.comment import CommentView
from .views.sci import SciTestView


def register_blueprints(app):
    app.register_blueprint(identity.identity, url_prefix='/auth')
    app.register_blueprint(PoemView.poem, url_prefix='/poem')
    app.register_blueprint(UserView.user, url_prefix='/user')
    app.register_blueprint(DwzView.dwz, url_prefix='/dwz')
    app.register_blueprint(WordsView.words, url_prefix='/words')
    app.register_blueprint(AdminView.admin, url_prefix='/admin')
    app.register_blueprint(CommentView.comment, url_prefix='/comment')
    app.register_blueprint(SciTestView.sci, url_prefix='/sci')
