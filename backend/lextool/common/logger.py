#!/usr/bin/env python3
# -*- coding:utf-8 -*-


r"""python log with color
log.py
    log module
Usage:
    from log import logger
    logger.debug("Hello World")
"""
import os
import sys
import time
import logging
import logging.handlers

from ..config.config import Cfg

log_level = 'DEBUG' if  Cfg.TOOLS.debug else 'INFO'
platform = 'win32'
platform = sys.platform
if platform == 'win32':
    log_path = 'J:\log'
else:
    log_path = Cfg.DEFAULT.log

STDOUT_LOG_FMT = "%(log_color)s[%(asctime)s] [%(levelname)s] [%(threadName)s] [%(filename)s:%(lineno)d] %(message)s"
STDOUT_DATE_FMT = "%Y-%m-%d %H:%M:%S"
FILE_LOG_FMT = "[%(asctime)s] [%(levelname)s] [%(threadName)s] [%(filename)s:%(lineno)d] %(message)s"
FILE_DATE_FMT = "%Y-%m-%d %H:%M:%S"


def _get_logger():

    _logger = logging.getLogger(__name__)

    stdout_handler = logging.StreamHandler()
    _logger.addHandler(stdout_handler)

    try:
        os.makedirs(log_path)
    except OSError:
        pass
    log_filename = time.strftime('%Y%m%d', time.localtime(time.time())) + '-server.log'
    log_file_path = os.path.join(log_path, log_filename)
    
    file_handler = logging.handlers.TimedRotatingFileHandler(
        log_file_path, when="midnight", backupCount=30, encoding='utf-8'
    )
    file_formatter = logging.Formatter(
        fmt=FILE_LOG_FMT,
        datefmt=FILE_DATE_FMT,
    )
    file_handler.setFormatter(file_formatter)
    _logger.addHandler(file_handler)

    _logger.setLevel(log_level)
    return _logger


LOG = _get_logger()