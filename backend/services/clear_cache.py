from flask_caching import Cache

from main import app, FILESYSTEM
from logger import logger

cache = Cache()


def main():
    cache.init_app(app, config=FILESYSTEM)

    with app.app_context():
        cache.clear()

if __name__ == '__main__':
    main()
    logger.info("done")