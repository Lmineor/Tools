#encoding:utf-8


def __get_domain(raw_input):
    if not raw_input.endswith('/'):
        raw_input += '/'
    pattern = "((http://)|(https://))?([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}(/)"
    domain = re.match(pattern, raw_input).group() if re.match(pattern, raw_input) else None
    routers = raw_input[len(domain)+1:] if len(domain) != len(raw_input) else ''
    return domain, routers


def __shorten(origin):
    res = __10to62(origin)
    return res


def __10to62(num):
    """
    10进制转62进制
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
    res = ''
    while num > base_scale-1:
        remainder = num % base_scale
        res += chars[remainder]
        num = num // base_scale
    res += chars[num]
    if len(res) < 6:
        for _ in range(6-len(res)):
            res = '0' + res
    return res

def shorturl(origin):
    '''
    origin: 数据库的递增字段
    '''
    su = __shorten(origin)
    return su


if __name__ == '__main__':
    print(__10to62(10005555))