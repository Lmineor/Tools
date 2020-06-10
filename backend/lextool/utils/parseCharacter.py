# encoding:utf-8
from ..config.default import DefaultConfig

def parseSpelling(spelling):
    if not spelling:
        return ''
    spelling.replace('\\\'', '\'')
    for k, v in DefaultConfig.SpecialChar.items():
        if k in spelling:
            spelling = spelling.replace(k, v)
    return spelling