import functools

from flask_caching import Cache

from .response import success_resp

cache = Cache()


# def return_if_has_cache(f):
#     @functools.wraps()

def return_if_has_cache(*args, **kwargs):
    """a decorater for return the cached data if exist"""
    def inner_func(func):
        @functools.wraps(func)
        def make_decorater():
            if cache.get(args):
                return success_resp(cache.get(args))
            else:
                func()
        return make_decorater
    return inner_func
