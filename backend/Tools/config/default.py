# encoding:utf-8


class DefaultConfig(object):
	SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/shorturl' # 默认数据库
	# 需要绑定的多个数据库
	SQLALCHEMY_BINDS = {
		'poem': 'mysql://root:123456@localhost:3306/poem',
		'user': 'mysql://root:123456@localhost:3306/user',
	}
	PER_PAGE = 30  # 分页每页的个数
	SECRET_KEY = '1Sv65NgaCm712i&6zSGFBr$XYvGUY%4R'

	# 缓存配置（文件系统缓存）
	FILESYSTEM = {
		'CACHE_TYPE': 'filesystem',
		'CACHE_DIR': './flask_cache',
		'CACHE_DEFAULT_TIMEOUT': 922337203685477580,
		'CACHE_THRESHOLD': 922337203685477580
	}
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	SESSION_TIME = 30*60
	EXPIRATION = 60*60*24  # auth有效期 1天
