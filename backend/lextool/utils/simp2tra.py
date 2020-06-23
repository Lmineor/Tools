#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 2020/6/23 10:21
@Author  : lex(luohai2233@163.com)
@File    : simp2tra.py
@Software: PyCharm

将简体中文转换成繁体中文
"""

import zhconv


def simp2tra(simp):
    return zhconv.convert(simp, 'zh-tw')
