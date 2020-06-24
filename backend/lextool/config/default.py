#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author  : lex(luohai2233@163.com)
@File    : default.py
"""

import os

try:
    from .local_config import *
except ImportError:
    pass


class DefaultConfig(object):

    # Default Database URI
    SQLALCHEMY_DATABASE_URI = 'mysql://{username}:{password}@localhost:3306/{db}'.format(**Default_DB)

    # multidb to bind
    SQLALCHEMY_BINDS = {'{db}'.format(**item):'mysql://{username}:{password}@localhost:3306/{db}'.format(**item) for item in BINDS_DB}


    # Pagination Number
    PER_PAGE = 15

    # Secret Key for Token
    SECRET_KEY = SECRET_KEY

    # Cache(for file cache)
    FILESYSTEM = {
		'CACHE_TYPE': 'filesystem',
		'CACHE_DIR': './flask_cache',
		'CACHE_DEFAULT_TIMEOUT': 922337203685477580,
		'CACHE_THRESHOLD': 922337203685477580
	}

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    # token valid time
    EXPIRATION = 60*60*1 # 1 hour
    LOGPATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    SpecialChar = {'&#230;': 'æ'}
    
    # Domain for verify token by url
    Domain = Domain
    
    # After verify token, redirect to login router
    FrontDomain = FrontDomain
    
    # Mail config
    MAIL_HOST = MAIL_HOST  # mail host
    MAIL_USER = MAIL_USER # mail user
    MAIL_PASS = MAIL_PASS  # mail password
    
    # English Words Book
    WORDSBOOK = ['CET4', 'CET6', 'TOEFL', 'GRE']
