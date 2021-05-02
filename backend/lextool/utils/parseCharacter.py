from backend.lextool.common.constants import SpecialChar


def parseSpelling(spelling):
    if not spelling:
        return ''
    spelling.replace('\\\'', '\'')
    for k, v in SpecialChar.items():
        if k in spelling:
            spelling = spelling.replace(k, v)
    return spelling