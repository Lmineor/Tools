# encoding:utf-8
# default config file
import os

try:
    from .local_config import SQLALCHEMY_BINDS, SQLALCHEMY_DATABASE_URI, SECRET_KEY
except ImportError:
    pass
except Exception as e:
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_BINDS = None
    SECRET_KEY = None
    raise e


class DefaultConfig(object):

    # Default Database URI
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI

    # 需要绑定的多个数据库
    SQLALCHEMY_BINDS = SQLALCHEMY_BINDS

    # Pagination Number
    PER_PAGE = 30  # 分页每页的个数

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
    
    SESSION_TIME = 30*60 
    
    EXPIRATION = 60*60*24  # auth有效期1天
    
    LOGPATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


if __name__ == '__main__':
    print(DefaultConfig.LOGPATH)