#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 2020/12/12 21:04
@Author  : lex(luohai2233@163.com)

The module to parse the config file
"""
import os
import configparser

from ..common.exceptions import ConfigFileNotFoundError


config_default = {
    'DEFAULT':
        {'debug': False, 'log_path': '/var/log/lextools'},
    'DB':
        {'username': None, 'password': None, 'database': None, 'sqlalchemy_track_modifications': True},
    'TOOLS':
        {'pagination': 10},
    'MAIL':
        {'username': None, 'password': None, 'host': None, 'domain':'127.0.0.1:5000', 'front_domain': '127.0.0.1:3000'},
    'AUTH':
        {'token_expiration': 3600, 'secret_key': None},
    'CACHE':
        {'type': 'filesystem', 'dir': './flask_cache', 'threshold':922337203685477580, 'default_timeout': 8640},
    'ENGLISH':
        {'word': []}
}


class DictAttr(object):
    """
    set attr for dict obj
    """ 

    def __init__(self, dict_obj):
        self.dict_obj = dict_obj
        for k, v in dict_obj.items():
            if k == 'ENGLISH':
                if v:
                    setattr(self, k, v.split(','))
            elif  k == 'debug':
                if v in ['False', 'false', False]:
                    setattr(self, k, False)
                elif v in ['True', 'true', True]:
                    setattr(self, k, True)
                else:
                    raise Exception("Debug option wrong, check it")
            else:
                setattr(self, k, v)

    def __getitem__(self, item):
        if self.dict_obj.get(item):
            return self.dict_obj.get(item)


class Config(object):
    def __init__(self):
        self.set_default_val()
        self._conf_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.ini')
        self.config_parser = configparser.ConfigParser()
        if os.path.exists(self._conf_path):
            self.config_parser.read(self._conf_path, encoding="utf-8")
        else:
            raise ConfigFileNotFoundError(self._conf_path)
        self.parser()
    
    def parser(self):
        sections = self.get_sections()
        for section in sections:
            items = self.get_items(section)
            setattr(self, section, DictAttr(dict(items)))      

    def set_default_val(self):
        for k, v in config_default.items():
            setattr(self, k, DictAttr(v))

    def get_sections(self):
        return self.config_parser.sections()
    
    def get_items(self, section):
        return self.config_parser.items(section)
    
    def __getitem__(self, item):
        return self.get_items(item)

Cfg = Config()
