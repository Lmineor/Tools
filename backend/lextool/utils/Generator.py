# encoding:utf-8
import re


class UidGenerator(object):
    """
    短网址(uid)生成
    """
    base_scale = 62
    chars = [
            '3', 'a', '7', 'n', '2', 'b', 'H', 'm', 'E', '4', 's',
            'M', 'f', 'Z', 'I', 'Y', 'K', 'x', 'q', 'U', 'o', 'l',
            'L', 'D', '5', 'd', 'Q', 'h', 'i', 'y', 'J', 'k', 't',
            'c', 'w', 'A', 'O', 'T', 'u', 'e', '6', '8', 'j', 'G',
            'C', 'V', 'N', 'z', 'X', 'S', 'F', '1', 'P', '9', 'B',
            '0', 'p', 'v', 'W', 'R', 'g', 'r'
    ]

    @classmethod
    def generate(cls, token):
        res = ''
        while token > cls.base_scale - 1:
            remainder = token % cls.base_scale
            res += cls.chars[remainder]
            token = token // cls.base_scale
        res += cls.chars[token]
        if len(res) < 6:
            for _ in range(6 - len(res)):
                res = '0' + res
        return res


class DWZGenerator(UidGenerator):
    def __init__(self):
        super(DWZGenerator, self).__init__()

    def __get_domain(self, url):
        if not url.endswith('/'):
            url += '/'
        pattern = "((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/)"
        domain = re.match(pattern, url).group() if re.match(pattern, url) else None
        routers = url[len(domain) + 1:] if len(domain) != len(url) else ''
        return domain, routers