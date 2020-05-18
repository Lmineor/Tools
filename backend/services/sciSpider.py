from multiprocessing import Process, Manager

import requests
from bs4 import BeautifulSoup

from logger import logger


class Sci(object):
    # 多进程版本的
    def __init__(self):
        self.url = 'http://www.howsci.com/sci-hub-alternative.html'
        self.parser = 'html.parser'
        self.__raw_url = []
        self.available_url = []

    def __drink_soup(self):
        req = requests.get(self.url, timeout=1000)
        req.encoding = 'utf-8'
        soup = BeautifulSoup(req.text, self.parser)
        return soup

    def __get_scis(self):
        logger.info("开始查询sci信息")
        soup = self.__drink_soup()
        a_list = soup.select('#post-2959 > div.entry-content > ol > li')
        for li in a_list:
            title = li.find('a').string
            if title:
                self.__raw_url.append(str(title))
        logger.info('完成sci查询')

    def raw_url(self):
        self.__get_scis()
        return self.__raw_url

    def detect_url(self):
        self.__get_scis()
        for url in self.raw_url:
            print(url)
            try:
                request = requests.get(url, timeout=500)
                if request.status_code == 200:
                    self.available_url.append(url)
                else:
                    logger.error(url + " " + "不可用")
            except Exception as e:
                pass
            finally:
                pass
        return self.available_url

if __name__ == '__main__':
    sci = Sci()
    ur = sci.raw_url()
    for i in ur:
        print(i)