import requests
import re
import MySQLdb
import time
import random
import os
from multiprocessing import Process, Queue

class BingDictSpider:
    def __init__(self, url):
        super(BingDictSpider, self).__init__()
        self.url = url
        self.q = Queue()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36',
        }

    def run(self):
         while not self.q.empty():
            data = self.q.get(timeout=30)
            self.__parse_page(data)

    def __send_request(self, target):
        '''
        用来发送请求的方法
        :return: 返回网页源码
        '''
        # 请求出错时，重复请求３次,
        i = 0
        while i <= 3:
            try:
                time.sleep(random.uniform(0,1.1))
                html = requests.get(url=self.url + target[1], timeout=1000, headers=self.headers).text
            except Exception as e:
                print('[INFO] %s'% e)
                i += 1
            else:
                return html

    def __parse_page(self, target):
        '''
        解析网站源码
        :return:
        '''
        print(target)
        response = self.__send_request(target)
        regularExpression = r'<div\s+class="hd_prUS b_primtxt">美&#160;(.+?)</div>'  # /([^\/]*)/
        matchObject = re.search(regularExpression, response, re.I)

        phoneticSpelling = ""
        if matchObject:
            if matchObject.group(1):
                phoneticSpelling = matchObject.group(1)
        if phoneticSpelling.startswith('['):
            sql_update = "UPDATE `enwords` SET `spelling` = '%s' WHERE `id` = %d" % (phoneticSpelling.replace('\'', '\\\''), target[0])
            self.update_sql(sql_update)
        else:
            print('Nothing')
            sql_update = "UPDATE `enwords` SET `spelling` = '%s' WHERE `id` = %d" % ('', target[0])
            self.update_sql(sql_update)

    def update_sql(self, sql_update):
        try:
            cur.execute(sql_update)
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()

    def putData(self, lst):
        for i in lst:
            self.q.put(i)
def generate_data():
    total = 103981
    for i in range(1, 10000):
        sql = "SELECT * FROM enwords WHERE id = %s" % i
        try:
            cur.execute(sql)
            # 获取所有记录列表
            result = cur.fetchone()
            yield (i,result[0])
        except:
            pass

dataGenerator = generate_data()

# 打开数据库连接
conn = MySQLdb.connect(host="127.0.0.1", port=3306, user="root", passwd="123456", db="words", charset='utf8')
cur = conn.cursor()


if __name__ == '__main__':
    url = "https://cn.bing.com/dict/search?q="
    spider = BingDictSpider(url=url)
    # dataGenerator = spider.generate_data()
    
    for j in range(100):
        lst = []
        for i in range(100):
            lst.append(next(dataGenerator))
        spider.putData(lst)
        Process_list = []
        # 创建并启动进程
        for i in range(6):
            p = Process(target = spider.run, args = ())
            p.start()
            print(os.getpid())
            Process_list.append(p)

        # 让主进程等待子进程执行完成
        for i in Process_list:
            i.join()
