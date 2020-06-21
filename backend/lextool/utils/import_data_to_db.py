import requests
import re
import MySQLdb
import time
import random

# 打开数据库连接
conn = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="words", charset='utf8')
cur = conn.cursor()


def insert_data(data):
    param = []
    for i in data:
        if len(i.split('\\')) > 3:
            print(i)
            word = i.split('\\')[0]
            splelA = i.split('\\')[1] + i.split('\\')[2]
            trans = i.split('\\')[3]
        elif len(i.split('\\')) < 3:
            print(i)
        else:
            word, splelA, trans = i.split('\\')
        param.append([None, word, trans, splelA, None])
    try:
        sql = 'INSERT INTO gre values(%s, %s, %s, %s, %s)'
        cur.executemany(sql, param)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()

def update_sql(sql):
    try:
        print(sql)
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()


def loadData():
    filename = r'C:\Users\Lex\Desktop\english-wordlists-master\GRE_8000_Words.txt'
    with open(filename, encoding='utf-8', mode='r') as f:
        data = f.read().splitlines()
    return data

data = loadData()
insert_data(data)

if cur:
    cur.close()
if conn:
    conn.close()




# if __name__ == '__main__':
#     data = loadData()
#     insert_data(data)