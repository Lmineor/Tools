#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 2020/12/26 21:23
@Author  : lex(luohai2233@163.com)
"""

from flask import jsonify
from .constants import SUCCESS_CODE, NOTFOUND_CODE


def not_found_resp(data):
    """
    the func of fail
    data: the data to return
    """
    return jsonify({
        'code': NOTFOUND_CODE,
        'description': 'The info you request does not exist...',
        'request_data': data
    })


def success_resp(req_info, data):
    """
    the func of success
    req_info: request info
    data: the data to return
    """
    # resp_body = req_info
    # resp_body.update(data)
    return jsonify({'code': SUCCESS_CODE, 'data': data})
