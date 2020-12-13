import datetime

from flask import Flask
from flask_cors import CORS

from .config.config import Cfg
from .register_blueprints import register_blueprints
from .common.cache import cache
from .common.logger import LOG
from .models import db


__version__ = '1.0'
__status__ = 'dev'
__description__ = 'tools'
__github__ = 'https://github.com/Prolht/Tools'
__license__ = "MIT License"


def create_app():
    LOG.debug('Starting Lextools...')
    app = Flask(__name__)
    # 数据库配置
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' \
                                            '%s:%s@localhost' \
                                            ':3306/%s' % (Cfg.DB.username, Cfg.DB.password, Cfg.DB.database)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Cfg.DB.sqlalchemy_track_modifications
    app.config['SECRET_KEY'] = Cfg.AUTH.secret_key
    register_blueprint(app)
    register_database(app)
    if Cfg.CACHE.type == 'filesystem':
        filesystem = {
            'CACHE_TYPE': Cfg.CACHE.type,
            'CACHE_DIR': Cfg.CACHE.dir,
            'CACHE_DEFAULT_TIMEOUT': Cfg.CACHE.default_timeout,
            'CACHE_THRESHOLD': Cfg.CACHE.threshold
        }
        cache.init_app(app, config=filesystem)
    CORS(app, supports_credentials=True)
    return app


def register_database(app):
    db.init_app(app)
    db.app = app


def register_blueprint(app):
    register_blueprints(app)
