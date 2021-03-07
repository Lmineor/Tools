#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Time    : 2020/12/12 21:04
@Author  : lex(luohai2233@163.com)

The module to parse the config file
"""
import os
import copy
import configparser

from ..common.exceptions import ConfigFileNotFoundError, InvaildOption
from ..common.constants import CONFIGFILE


config_default = {
    'DB':
        {'username': None, 'password': None, 'database': None, 'sqlalchemy_track_modifications': True},
    'TOOLS':
        {'pagination': 10, 'debug': False, 'log_path': '../../log'},
    'MAIL':
        {'username': None, 'password': None, 'host': None, 'domain':'127.0.0.1:5000', 'front_domain': '127.0.0.1:3000'},
    'AUTH':
        {'token_expiration': 3600, 'secret_key': None},
    'CACHE':
        {'type': 'filesystem', 'dir': './flask_cache', 'threshold':922337203685477580, 'default_timeout': 8640},
    'ENGLISH':
        {'word': []}
}

config_op = copy.deepcopy(config_default)

def update_default_config(section, options):
    for k, v in options.items():
        config_op[section][k] = v
    

class DictAttr(object):
    """
    set attr for dict obj
    """ 

    def __init__(self, dict_obj):
        self.dict_obj = dict_obj
        self.validate()
        for k, v in self.dict_obj.items():
            setattr(self, k, v)

    def validate(self):
        for k, v in self.dict_obj.items():
            if k == 'ENGLISH':
                if v:
                    self.dict_obj[k] = v.split(',')
            elif  k == 'debug':
                if v in ['False', 'false', False]:
                    self.dict_obj[k] = False
                elif v in ['True', 'true', True]:
                    self.dict_obj[k] = True
                else:
                    raise Exception("Debug option wrong, Check it")
            elif k in ['token_expiration', 'threshold', 'pagination', 'default_timeout']:
                try:
                    self.dict_obj[k] = int(v)
                except ValueError:
                    raise InvaildOption(k, v)
            else:
                pass

    def __getitem__(self, item):
        if self.dict_obj.get(item):
            return self.dict_obj.get(item)


class Config(object):
    def __init__(self):
        self._conf_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), CONFIGFILE)
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
            update_default_config(section, dict(items))
            setattr(self, section, DictAttr(config_op[section]))

    def get_sections(self):
        return self.config_parser.sections()
    
    def get_items(self, section):
        return self.config_parser.items(section)
    
    def __getitem__(self, item):
        return self.get_items(item)

Cfg = Config()
