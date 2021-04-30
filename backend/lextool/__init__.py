import datetime

from flask import Flask
from flask_cors import CORS
from oocfg import cfg

from .register_blueprints import register_blueprints
from .common.cache import cache
from .common.logger import _get_logger
from .models import db


__version__ = '1.0'
__status__ = 'dev'
__description__ = 'tools'
__github__ = 'https://github.com/Prolht/Tools'
__license__ = "MIT License"


LOG = _get_logger()


def create_app():
    LOG.debug('Starting Lextools...')
    app = Flask(__name__)
    # 数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' \
                                            '%s:%s@localhost' \
                                            ':3306/%s' % (cfg.CONF.DB.username, cfg.CONF.DB.password, cfg.CONF.DB.database)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = cfg.CONF.DB.sqlalchemy_track_modifications
    app.config['SECRET_KEY'] = cfg.CONF.AUTH.secret_key
    register_blueprint(app)
    register_database(app)
    if cfg.CONF.CACHE.type == 'filesystem':
        filesystem = {
            'CACHE_TYPE': cfg.CONF.CACHE.type,
            'CACHE_DIR': cfg.CONF.CACHE.dir,
            'CACHE_DEFAULT_TIMEOUT': cfg.CONF.CACHE.default_timeout,
            'CACHE_THRESHOLD': cfg.CONF.CACHE.threshold
        }
        cache.init_app(app, config=filesystem)
    CORS(app, supports_credentials=True)
    return app


def register_database(app):
    db.init_app(app)
    db.app = app


def register_blueprint(app):
    register_blueprints(app)
