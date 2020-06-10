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
        regularExpressionE = r'<div\s+class="hd_pr b_primtxt">英&#160;(.+?)</div>'  # /([^\/]*)/
        regularExpressionA = r'<div\s+class="hd_prUS b_primtxt">美&#160;(.+?)</div>'  # /([^\/]*)/
        matchObjectE = re.search(regularExpressionE, response, re.I)
        matchObjectA = re.search(regularExpressionA, response, re.I)

        phoneticSpellingE = ""
        phoneticSpellingA = ""
        if matchObjectE:
            if matchObjectE.group(1):
                phoneticSpellingE = matchObjectE.group(1)
        if phoneticSpellingE.startswith('['):
            sql_updateE = "UPDATE `cet6` SET `spellingE` = '%s' WHERE `id` = %d" % (phoneticSpellingE.replace('\'', '\\\''), target[0])
            self.update_sql(sql_updateE)
        else:
            print('Nothing')
            sql_updateE = "UPDATE `cet6` SET `spellingE` = '%s' WHERE `id` = %d" % ('', target[0])
            self.update_sql(sql_updateE)


        if matchObjectA:
            if matchObjectA.group(1):
                phoneticSpellingA = matchObjectA.group(1)
        if phoneticSpellingA.startswith('['):
            sql_updateA = "UPDATE `cet6` SET `spellingA` = '%s' WHERE `id` = %d" % (phoneticSpellingA.replace('\'', '\\\''), target[0])
            self.update_sql(sql_updateA)
        else:
            print('Nothing')
            sql_updateA = "UPDATE `cet6` SET `spellingA` = '%s' WHERE `id` = %d" % ('', target[0])
            self.update_sql(sql_updateA)

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
    total = 2089
    for i in range(1, total+1):
        sql = "SELECT * FROM cet6 WHERE id = %s" % i
        try:
            cur.execute(sql)
            # 获取所有记录列表
            result = cur.fetchone()
            yield (i,result[1])
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
    
    # for j in range(5):
    lst = []
    for i in range(1, 2090):
        try:
            lst.append(next(dataGenerator))
        except Exception as e:
            print(e)
            break
    spider.putData(lst)
    Process_list = []
    # 创建并启动进程
    for i in range(10):
        p = Process(target = spider.run, args = ())
        p.start()
        print(os.getpid())
        Process_list.append(p)

    # 让主进程等待子进程执行完成
    for i in Process_list:
        i.join()

