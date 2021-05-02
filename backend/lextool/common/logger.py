#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import sys
import time
import logging
import logging.handlers

from oocfg import cfg


def _get_logger():
    log_level = 'DEBUG' if cfg.CONF.TOOLS.debug else 'INFO'

    platform = sys.platform
    if platform == 'win32':
        log_path = 'J:\log'
    else:
        log_path = cfg.CONF.TOOLS.log_path

    STDOUT_LOG_FMT = "%(log_color)s[%(asctime)s] [%(levelname)s] [%(threadName)s] [%(filename)s:%(lineno)d] %(message)s"
    STDOUT_DATE_FMT = "%Y-%m-%d %H:%M:%S"
    FILE_LOG_FMT = "[%(asctime)s] [%(levelname)s] [%(threadName)s] [%(filename)s:%(lineno)d] %(message)s"
    FILE_DATE_FMT = "%Y-%m-%d %H:%M:%S"

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