# encoding:utf-8
# default config file
import os

try:
    from .local_config import *
except ImportError:
    pass


class DefaultConfig(object):

    # Default Database URI
    SQLALCHEMY_DATABASE_URI = 'mysql://{username}:{password}@localhost:3306/{db}'.format(**Default_DB)

    # 需要绑定的多个数据库
    SQLALCHEMY_BINDS = {'{db}'.format(**item):'mysql://{username}:{password}@localhost:3306/{db}'.format(**item) for item in BINDS_DB}


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
    
    
    # EXPIRATION = 30  # auth有效期1小时
    EXPIRATION = 60*60*1  # auth有效期1小时
    LOGPATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    SpecialChar = {'&#230;': 'æ'}

    Domain = Domain
    FrontDomain = FrontDomain
    MAIL_HOST = MAIL_HOST  # 设置服务器
    MAIL_USER = MAIL_USER  # 用户名
    MAIL_PASS = MAIL_PASS  # 口令


if __name__ == '__main__':
    print(DefaultConfig.LOGPATH)