#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 2020/12/26 21:23
@Author  : lex(luohai2233@163.com)
"""

from flask import jsonify
from .constants import SUCCESS_CODE, NOTFOUND_CODE


def not_found_resp(data):
    return jsonify({
        'code': NOTFOUND_CODE,
        'description': 'The info you request does not exist...',
        'request_data': data
    })
        

def success_resp(data):
    return jsonify({'code': SUCCESS_CODE, 'data': data})
    