from oocfg import cfg, options

# Belows are config options
cfg_group = {}

db_options = [
    options.StrOpt('username', default='username', helper='this is username'),
    options.StrOpt('password', default='123456', helper='database password'),
    options.StrOpt('database', default='tools', helper='database name'),
    options.BoolOpt('sqlalchemy_track_modifications', default=True, helper='sqlalchemy_track_modifications')
    ]
cfg_group['db'] = db_options

tools_options = [
    options.IntOpt('pagination', default=10, helper='per page item'),
    options.BoolOpt('debug', default=False, helper='debug mode'),
    options.StrOpt('log_path', default='../../log', helper='log path')
]
cfg_group['tools'] = tools_options

mail_options = [
    options.StrOpt('username', default='example@example.com', helper='mail service username'),
    options.StrOpt('password', default='123456', helper='mail service password'),
    options.StrOpt('host', default='', helper='host'),
    options.StrOpt('domain', default='127.0.0.1:5000', helper='backend domain'),
    options.StrOpt('front_domain', default='127.0.0.1:3000', helper='frontend domain')
]
cfg_group['mail'] = mail_options

auth_options = [
    options.IntOpt('token_expiration', default=3600, helper='the time of token expire'),
    options.StrOpt('secret_key', default='', helper='secret_key')
]
cfg_group['auth'] = auth_options

cache_options = [
    options.StrOpt('type', default='filesystem', choices=['filesystem', 'other'], helper='the type of cache'),
    options.StrOpt('dir', default='./flask_cache', helper='cache dir'),
    options.IntOpt('threshold', default=922337203685477580, helper='threshold'),
    options.IntOpt('default_timeout', default=8640, helper='default time out')
]
cfg_group['cache'] = cache_options


eng_options = [
    options.ListOpt('word', default=[], helper='word')
]
cfg_group['english'] = eng_options


def run_server():
    from backend.lextool import create_app
    from backend.lextool.common.logger import LOG

    app = create_app()
    debug = cfg.CONF.TOOLS.debug
    LOG.info("Running server...")
    app.run(debug=debug)


def init_config():
    cfg.startup(cfg_group, config_file='/Users/lex/code/coding/Tools/backend/lextool/config.ini')


init_config()
run_server()
