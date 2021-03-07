import requests
import re
import os
import json

import MySQLdb
import time
import random

from Generator import UidGenerator

# 打开数据库连接
# conn = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="words", charset='utf8')
# cur = conn.cursor()


UID_INDEX = 1

class Connect(object):
    def __init__(self):
        self.connect(user='root', password='1qaz@WSX', db='tools')

    def connect(self, user, password, db, host="127.0.0.1", port=3306, charset='utf8'):
        self.conn = MySQLdb.connect(host=host, port=port, user=user, password=password, db=db, charset=charset)
        self.cur = self.conn.cursor()


class DataProcess(object):
    def __init__(self):
        self.file_path = '/Users/lex/code/chinese-poetry-master'
        self.db = Connect()
        self.conn = self.db.conn
        self.cur = self.db.cur

        self.find_shi_file()

    def load_data(self, filename):
        with open(filename, 'r') as f:
            data = f.read()
        return json.loads(data)

    def process_ci_data(self):
        for i in range(0, 21050, 1000):
            ci_file_path = os.path.join(self.file_path, 'ci')
            filename = os.path.join(ci_file_path, 'ci.song.%s.json' % i)
            data = self.load_data(filename)

    def find_shi_file(self):
        shi_path = os.path.join(self.file_path, 'json')
        files_in_shi_path = os.listdir(shi_path)
        tangshi_files = []
        songshi_files = []

        for file in files_in_shi_path:
            if file.startswith('poet.tang'):
                tangshi_files.append(os.path.join(shi_path,file))
            if file.startswith('poet.song'):
                songshi_files.append(os.path.join(shi_path,file))
        tangshi_author_file = os.path.join(shi_path, 'authors.tang.json')
        songshi_author_file = os.path.join(shi_path, 'authors.song.json')

        self.tangshi_files = tangshi_files
        self.songshi_files = songshi_files
        self.tangshi_author_file = tangshi_author_file
        self.songshi_author_file = songshi_author_file

        # return tangshi_files, songshi_files, tangshi_author_file, songshi_author_file

    def process_tangshi_data(self):
        for tangshi_file in self.tangshi_files:
            data = self.load_data(tangshi_file)
            self.insert_tangshi_data(data)

    def insert_like_shi(self, uid):
        sql = """
        INSERT INTO
        like_poem
        (i_like, uid)
        VALUES
        ('%s', '%s')
        """
        self.cur.execute(sql % (0, uid))

    def insert_tangshi_data(self, data):
        sql = """INSERT INTO
        poems
        (paragraphs, poem, poet_id, u_id)
        VALUES
        ('%(paragraphs)s', '%(poem)s' ,'%(poet_id)s', '%(u_id)s')"""
        global UID_INDEX
        body = {}
        for poem in data:
            body['paragraphs'] = '｜'.join(poem['paragraphs'])
            body['poem'] = poem['title']
            poet_id = self.fetch_poet_id(poem['author'])
            if poet_id is None:
                continue
            body['poet_id'] = self.fetch_poet_id(poem['author'])
            uid = UidGenerator.generate(UID_INDEX)
            UID_INDEX += 1

            body['u_id'] = uid

            try:
                self.insert_like_shi(uid)
                self.cur.execute(sql % body)
            except Exception as E:
                print(body)
                print(E)
                UID_INDEX -= 1
            body = {}
        self.conn.commit()

    def fetch_poet_id(self, poet):
        sql = "SELECT p.id FROM poets AS p WHERE poet='%s'"
        self.cur.execute(sql % poet)
        try:
            return self.cur.fetchone()[0]
        except:
            return None

    def insert_poet_data(self, dynasty):
        sql = """
        INSERT INTO
        poets
        (poet, dynasty, descb)
        VALUES
        ('%(poet)s', '%(dynasty)s', '%(descb)s')
        """
        if dynasty == '宋':
            poets = self.load_data(self.songshi_author_file)
        else:
            poets = self.load_data(self.tangshi_author_file)

        body = {}
        for poet in poets:
            body['descb'] = poet['desc']
            body['poet'] = poet['name']
            body['dynasty'] = dynasty
            try:
                self.cur.execute(sql % body)
            except Exception as e:
                print(body)
            body = {}
        self.conn.commit()

dp = DataProcess()

# dp.insert_poet_data('唐')
dp.process_tangshi_data()
