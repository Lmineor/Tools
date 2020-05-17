#encoding:utf-8

import hashlib
import re

from flask import request, redirect, Response
from flask_cors import CORS
from flask_caching import Cache

from db import *
from logger import logger
from gen_dwz import gen_dwz
from sciSpider import Sci
from local_config import PER_PAGE

# app 在db中
CORS(app, supports_credentials=True)
# ----------------------------------------------------------------
# 缓存配置（文件系统缓存）
FILESYSTEM = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': './flask_cache',
    'CACHE_DEFAULT_TIMEOUT': 2,
    # 'CACHE_DEFAULT_TIMEOUT': 922337203685477580,
    'CACHE_THRESHOLD': 922337203685477580
}
cache = Cache(app,config=FILESYSTEM)


# ----------------------------------------------------------------
# 路由
@app.route('/poem/getauthor', methods=['POST'])
def get_author():
    """
    得到某个朝代的作者列表
    """
    dynasty = request.get_json()['dynasty']
    page = request.get_json()['page']
    if cache.get(str(page) + dynasty):
        total = cache.get('authors_num' + dynasty)
        authors =  cache.get(str(page) + dynasty)
    else:
        try:
            if dynasty =='唐':
                total = len(PoemTangAuthor.query.all())
                items = PoemTangAuthor.query.paginate(page=page, per_page=PER_PAGE, error_out=False).items
                authors = list(set([item.name for item in items]))
            else:
                total = len(PoemSongAuthor.query.all())
                items = PoemSongAuthor.query.paginate(page=page, per_page=PER_PAGE, error_out=False).items
                authors = list(set([item.name for item in items]))
        except Exception as e:
            authors = []
            total = 0
            logger.error(e)
        cache.set('authors_num' + dynasty, total)
        cache.set(str(page) + dynasty, authors)
    data = {
        'code': 200,
        'total': total,
        'authors': authors
    }
    return data


@app.route('/poem/gettitle', methods=['POST'])
def get_title():
    """
    test
    """
    author = request.get_json()['author']
    dynasty = request.get_json()['dynasty']
    logger.info('author' + author)
    if cache.get(author + dynasty):
        titles = cache.get(author + dynasty)
    else:
        try:
            items = PoemTangSong.query.filter_by(author = author, dynasty=dynasty).all()
            titles = list(set([item.title for item in items]))
        except Exception as e:
            titles = []
            logger.error(e)
        cache.set(author + dynasty, titles)
    return {
        'code': 200,
        'titles': titles
    }


@app.route('/poem/getpoem', methods=['POST'])
def get_poem():
    """
    test
    """
    author = request.get_json()['author']
    dynasty = request.get_json()['dynasty']
    title = request.get_json()['title']
    logger.info('author' + author)
    if cache.get(author + dynasty + title):
        poem = cache.get(author + dynasty + title)
    else:
        try:
            poem = PoemTangSong.query.filter_by(author = author, dynasty=dynasty, title=title).first().paragraphs
        except Exception as e:
            poem = ''
            logger.error(e)
        cache.set(author + dynasty + title, poem)
    return {
        'code': 200,
        'poem': poem
    }

@app.route('/poem/lunyu', methods=['POST', 'GET'])
def get_lunyu():
    """
    test
    """
    if request.method == 'GET':
        if cache.get('chapters'):
            chapters = cache.get('chapters')
        else:
            try:
                items = PoemLunyu.query.all()
                print(items[0])
                chapters = list(set([item.chapter for item in items]))
            except Exception as e:
                chapters = []
                logger.error(e)
            cache.set('chapters', chapters)
        return {
            'code': 200,
            'chapters': chapters
        }
    else:
        chapter = request.get_json()['chapter']
        logger.info('chapter: ' + chapter)
        if cache.get('chapter'):
            paragraphs = cache.get('chapter')
        else:
            try:
                paragraphs = PoemLunyu.query.filter_by(chapter = chapter).first().paragraphs
            except Exception as e:
                paragraphs = ''
                logger.error(e)
            cache.set(chapter, paragraphs)
        return {
            'code': 200,
            'paragraphs': paragraphs.split('|')
        }


@app.route('/poem/songci', methods=['POST', 'GET'])
def get_songci():
    """
    test
    """
    author = request.get_json()['author']
    rhythmic = request.get_json()['rhythmic']
    page = request.get_json()['page']
    if page: # 获取作者翻页数据
        if cache.get('authors_num' + 'songci'):
            total = int(cache.get('authors_num' + 'songci'))
        else:
            total = len(CiAuthor.query.all())
            cache.set('authors_num' + 'songci', total)
        if cache.get(str(page) + 'songci'):
            authors =  cache.get(str(page) + 'songci')
        else:
            try:
                items = CiAuthor.query.paginate(page=page, per_page=PER_PAGE, error_out=False).items
                authors = list(set([item.name for item in items]))
            except Exception as e:
                authors = []
                logger.error(e)
            cache.set(str(page) + 'songci', authors)
        return {
            'code': 200,
            'authors': authors,
            'total': total
        }
    elif not rhythmic: # 获取词牌名s
        if cache.get(author + '_ci'):
            rhythmics = cache.get(author + '_ci')
        else:
            try:
                items = PoemSongci.query.filter_by(author = author).all()
                rhythmics = list(set([item.rhythmic for item in items]))
            except Exception as e:
                rhythmics = []
                logger.error(e)
            cache.set(author + '_ci', rhythmics)
        return {
            'code': 200,
            'rhythmics': rhythmics
        }
    else:
        if cache.get(author + rhythmic + '_ci'):
            paragraphs = cache.get(author + rhythmic + '_ci')
        else:
            try:
                paragraphs = PoemSongci.query.filter_by(author=author, rhythmic=rhythmic).first().paragraphs.split('。')
            except Exception as e:
                paragraphs = ''
                logger.error(e)
            cache.set(author + rhythmic + '_ci', paragraphs)
        return {
            'code': 200,
            'paragraphs': paragraphs
        }


@app.route('/shorturl/shorten', methods=['POST'])
def main():
    url = request.get_json()['url']
    logger.info('输入的url为：' + url)
    if not url:
        return None
    su = __pre_get(url)
    if su:
        return {
            'code': 200,
            'url': su
            }
    try:
        shortU = ShortUrl(origin_url = url)
        db.session.add(shortU)
        db.session.flush()
        urlid = shortU.id # 得到最后一调数据插入的id
        su = gen_dwz(urlid) # 生成短链
        logger.info("短链成功生成")
        shortU.short_url = su
        db.session.add(shortU)
        db.session.flush()
        db.session.commit()
    except Exception as e:
        logger.error(url + ' 重复')
        logger.error(e)
    if not su:
        item = ShortUrl.query.filter(ShortUrl.origin_url == url).first()
        if item:
            su = item.short_url
    data = {
        'code': 200,
        'url': su
    }
    return data


@app.route('/s/<code>', methods=['GET'])
def redir(code):
    """
    重定向部分
    """
    try:
        item = ShortUrl.query.filter(ShortUrl.short_url == str(code)).first()
        origin_url = item.origin_url
    except Exception as e:
        origin_url = ''
        logger.error(e)
    if not origin_url:
        return render_template('404.html')
    elif not origin_url.startswith('http'):
        return redirect('http://' + origin_url)
    else:
        return redirect(origin_url)


@app.route('/shorturl/OriginUrl', methods=['POST'])
def get_originurl():
    """
    短链还原部分
    """
    shorturl = request.get_json()['shorturl']
    logger.info('输入的shorturl为：' + shorturl)
    if not shorturl:
        return None;
    try:
        item = ShortUrl.query.filter(ShortUrl.short_url == shorturl).first()
        origin_url = item.origin_url
    except Exception as e:
        origin_url = ''
        logger.error(e)
    return {
        'code': 200,
        'OriginUrl': origin_url
    }


@app.route('/sci', methods=['GET'])
def get_sci():
    sci_url = Sci()
    urls = sci_url.raw_url()
    data = {
        'code': 200,
        'urls': urls
    }
    return data


def __pre_get(url):
    su = ''
    try:
        item = ShortUrl.query.filter(ShortUrl.origin_url == url).first()
        if item:
            su = item.short_url
    except Exception as e:
        logger.error(e)
    return su


if __name__ == '__main__':
    try:
        db.create_all()
    except Exception as e:
        pass
    app.run()
