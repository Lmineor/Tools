import logging
_g_logger = None


def get_logger():
    global _g_logger
    if _g_logger is None:
        __datetime = "%Y-%m-%d %H:%M:%S"
        __format_str = "%(asctime)s %(levelname).1s [%(filename)s:%(lineno)s] %(message)s"
        _g_logger = logging.getLogger()
        # stream header
        logging.basicConfig(filename='app.log')  # 制定log文件的存放位置
        formater = logging.Formatter(__format_str, __datetime)
        handler = logging.StreamHandler()
        handler.setFormatter(formater)
        _g_logger.addHandler(handler)
        _g_logger.setLevel(logging.DEBUG)
    return _g_logger


logger = get_logger()
