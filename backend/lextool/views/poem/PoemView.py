from functools import wraps
import json
import re

from flask import (Blueprint, request, jsonify, abort)

from ...models.poem import *
from ...common.cache import cache
from ...common.logger import LOG
from ...common.response import not_found_resp, success_resp
from ...config.config import Cfg
from ...utils.simp2tra import simp2tra
from ...common.exceptions import PoemNotFound


poem = Blueprint('poem', __name__)


def _make_cache_key(url, cache_info):
    cache_key = {'url': url}
    cache_key.update(cache_info)
    return json.dumps(cache_key)


@poem.route('/poets/', methods=['GET'])
def get_poets():
    """
    获取指定朝代的所有作者，若不指定朝代，则默认返回“唐”朝的作者信息
    """
    param = request.args
    req_path = request.path
    dynasty = param.get('dynasty', '唐')
    page = param.get('page', 1, type=int)
    per_page = param.get('per_page', Cfg.TOOLS.pagination, type=int)
    LOG.info("Get Poets of {} in page {}".format(dynasty, page))
    
    cache_key = _make_cache_key(
        req_path, {'dynasty': dynasty,'page': page,'per_page': per_page}
    )
    cache_data = cache.get(cache_key)
    
    if cache_data:
        data = cache_data
        LOG.info("Get Poets of {} in page {} by cache".format(dynasty, page))
        return jsonify(data)
    else:
        paginate_obj = PoetIntroduction.query.filter_by(dynasty=dynasty).paginate(
            page=page,
            per_page=per_page,
            error_out=True
        )
        if not paginate_obj.items:
            return not_found_resp({'poem': dynasty})
        data = {
            'total': paginate_obj.total,
            'poets': [item.poet for item in paginate_obj.items],
            'per_page': per_page,
            'has_next': paginate_obj.has_next,
            'has_prev': paginate_obj.has_prev,
            'dynasty': dynasty
        }
        cache.set(cache_key, data)
        return success_resp(data)


@poem.route('/poems/', methods=['GET'])
def get_poems():
    """
    获取诗人的诗作
    """
    param = request.args
    poet = simp2tra(param.get('poet', '李白'))
    dynasty = param.get('dynasty', '唐')
    cache_key = poet + dynasty + "poems"
    cache_data = cache.get(cache_key)
    if cache_data:
        LOG.info("Get {} {}'s Poems by cache".format(dynasty, poet))
        poems = cache_data
    else:
        try:
            LOG.info("Get {} {}'s Poems".format(dynasty, poet))
            items = PoemTangSong.query.filter_by(poet=poet, dynasty=dynasty).all()
            poems = [item.poem for item in items]
            cache.set(poet + dynasty + "poems", poems)
        except Exception as e:
            poems = []
            LOG.error("Error : {}".format(e))
    return jsonify({
        'code': 200,
        'poems': poems
    })


@poem.route('/search/', methods=['GET'])
def search_poets():
    """
    获取诗人的诗作
    """
    param = request.args
    keyword = simp2tra(param.get('keyword'))
    page = param.get('page', 1, type=int)
    LOG.info("Search Poets has {}".format(keyword))
    cache_key = '__poet_search' + keyword + str(page)
    cache_data = cache.get(cache_key)
    if not keyword or not isinstance(keyword, str):
        return jsonify({'code': 200, 'poets': []})
    if cache_data:
        data = json.loads(cache_data)
        poets = data['poets']
        total = data['total']
    else:
        try:
            poets = PoetIntroduction.search_poet(keyword, page)
            total = PoetIntroduction.search_keyword_total(keyword)
            cache.set('/poet/search' + keyword + str(page), poets)
            cache.set('/poet/search' + keyword + 'total', total)
        except Exception as e:
            poets = []
            total = 0
            LOG.error("Error : {}".format(e))
    return jsonify({
        'code': 200,
        'poets': poets,
        'total': total
    })


@poem.route('/content/', methods=['GET'])
def get_content():
    """
    获取诗歌内容
    """
    param = request.args
    poet = param.get('poet')
    dynasty = param.get('dynasty')
    title = param.get('poem')
    cache_key = title
    LOG.info("Get {}'s {}'s content".format(poet, poem))
    if cache.get(poet + dynasty + title):
        content = cache.get("content" + poet + dynasty + title)
    else:
        try:
            item = PoemTangSong.query.filter_by(
                    poet=poet,
                    dynasty=dynasty,
                    poem=title).first()
            content = re.split("。|？", item.paragraphs) if item else []
            cache.set("content" + poet + dynasty + title, content)
        except Exception as e:
            content = []
            LOG.error("Error is: {}".format(e))
    return jsonify({
        'code': 200,
        'content': content
    })


@poem.route('/lunyu/', methods=['GET'])
def get_lunyu():
    """
    test
    """
    param = request.args
    chapter = param.get('chapter')
    if not chapter:
        if cache.get('chapters'):
            chapters = cache.get('chapters')
        else:
            try:
                items = PoemLunyu.query.all()
                chapters = list(set([item.chapter for item in items]))
            except Exception as e:
                chapters = []
                LOG.error(e)
            cache.set('chapters', chapters)
        return jsonify({
            'code': 200,
            'chapters': chapters
        })
    else:
        LOG.info('chapter: ' + chapter)
        if cache.get('chapter'):
            paragraphs = cache.get('chapter')
        else:
            try:
                paragraphs = PoemLunyu.query.filter_by(chapter=chapter).first().paragraphs
            except Exception as e:
                paragraphs = ''
                LOG.error(e)
            cache.set(chapter, paragraphs)
        return jsonify({
            'code': 200,
            'paragraphs': paragraphs.split('|')
        })


@poem.route('/songci/', methods=['GET'])
def get_songci():
    """
    test
    """
    param = request.args
    poet = param.get('poet')
    rhythmic = param.get('rhythmic')
    page = param.get('page', 1, type=int)
    limits = param.get('limits', 0, type=int)
    cache_key = '__songCi' + 'page' + str(page) + 'limits' + str(limits) + poet + rhythmic
    cache_data = cache.get(cache_key)
    if cache_data:
        data = json.loads(cache_data)
        total = data['total']
        if page:                        # 若传page的参数，则说明要获取作者列表
            poets = data['poets']
        pass
    if page:  # 获取作者翻页数据
        page = int(page)
        if cache.get('poets_num' + 'songci'):
            total = int(cache.get('poets_num' + 'songci'))
        if cache.get(str(page) + 'songci'):
            poets = cache.get(str(page) + 'songci')
        else:
            try:
                items = CiAuthor.query.paginate(page=page, per_page=Cfg.TOOLS.pagination, error_out=False)
                total = items.total
                cache.set('poets_num' + 'songci', total)
                poets = list(set([item.poet for item in items.items]))
            except Exception as e:
                poets = []
                LOG.error(e)
            cache.set(str(page) + 'songci', poets)
        return jsonify({
            'code': 200,
            'poets': poets,
            'total': total
        })
    elif not rhythmic:  # 获取词牌名s
        if cache.get(poet + '_ci'):
            rhythmics = cache.get(poet + '_ci')
        else:
            try:
                items = PoemSongci.query.filter_by(poet=poet).all()
                rhythmics = list(set([item.rhythmic for item in items]))
            except Exception as e:
                rhythmics = []
                LOG.error(e)
            cache.set(poet + '_ci', rhythmics)
        return jsonify({
            'code': 200,
            'rhythmics': rhythmics
        })
    else:
        if cache.get(poet + rhythmic + '_ci'):
            paragraphs = cache.get(poet + rhythmic + '_ci')
        else:
            try:
                paragraphs = PoemSongci.query.filter_by(poet=poet, rhythmic=rhythmic).first().paragraphs.split('。')
            except Exception as e:
                paragraphs = ''
                LOG.error(e)
            cache.set(poet + rhythmic + '_ci', paragraphs)
        return jsonify({
            'code': 200,
            'paragraphs': paragraphs
        })


@poem.route('/songci/content/', methods=['GET'])
def get_songci_content():
    """
    test
    """
    param = request.args
    poet = param.get('poet')
    rhythmic = param.get('rhythmic')
    cache_key = '__songCi_content' + poet + rhythmic
    cache_data = cache.get(cache_key)
    if cache_data:
        LOG.info("GET SongCi Content By Cache")
        paragraphs = cache_data
    else:
        try:
            query_obj = PoemSongci.query.filter_by(poet=poet, rhythmic=rhythmic).first()
            paragraphs = re.split('。|？', query_obj.paragraphs)
            cache.set(cache_key, paragraphs)
        except Exception as e:
            paragraphs = ''
            LOG.error(e)
    return jsonify({
        'code': 200,
        'paragraphs': paragraphs
    })


@poem.route('/songci/poem/', methods=['GET'])
def get_songci_poem():
    """
    获取某个作者的词
    """
    param = request.args
    poet = param.get('poet')

    cache_key = '__songCi_poem' + 'poet:' + poet
    cache_data = cache.get(cache_key)
    if cache_data:
        LOG.info("GET By Cache Req {}".format(cache_key))
        rhythmics = cache_data
    else:
        try:
            items = PoemSongci.query.filter_by(poet=poet).all()
            rhythmics = [item.rhythmic for item in items]
        except Exception as e:
            rhythmics = []
            LOG.error(e)
        cache.set(cache_key, rhythmics)

    return jsonify({
            'code': 200,
            'rhythmics': rhythmics
        })


@poem.route('/songci/poets/', methods=['GET'])
def get_songci_poets():
    """
    test
    """
    param = request.args
    page = param.get('page', 0, type=int)
    limits = param.get('limits', 0, type=int)
    cache_key = '__songCi: ' + 'page: ' + str(page) + 'limits: ' + str(limits)
    LOG.info("GET {}".format(cache_key))
    cache_data = cache.get(cache_key)
    if cache_data:
        data = json.loads(cache_data)
        total = data['total']
        poets = data['poets']
    else:
        try:
            query_obj = CiAuthor.query.paginate(
                page=page,
                per_page=limits if limits else Cfg.TOOLS.pagination,
                error_out=False)
            total = query_obj.total
            poets = [item.poet for item in query_obj.items]
            cache_data = {'total': total, 'poets': poets}
            cache.set(cache_key, json.dumps(cache_data))
        except Exception as e:
            poets = []
            total = 0
            LOG.error(e)
        cache.set(str(page) + 'songci', poets)
    return jsonify({
        'code': 200,
        'poets': poets,
        'total': total
    })


@poem.route('/shijing/', methods=['GET'])
def get_shijing():
    """
    test
    """
    param = request.args
    poem = param.get('poem')
    page = param.get('page', 1, type=int)
    if page:  # 获取诗名翻页数据
        page = int(page)
        if cache.get('poem_num' + 'shijing'):
            total = int(cache.get('poem_num' + 'shijing'))
        else:
            total = len(ShiJing.query.all())
            cache.set('poem_num' + 'shijing', total)
        if cache.get(str(page) + 'shijing'):
            poems = cache.get(str(page) + 'shijing')
        else:
            try:
                items = ShiJing.query.paginate(page=page, per_page=Cfg.TOOLS.pagination, error_out=False).items
                poems = list(set([item.poem for item in items]))
            except Exception as e:
                poems = []
                LOG.error(e)
            cache.set(str(page) + 'shijing', poems)
        return jsonify({
            'code': 200,
            'poems': poems,
            'total': total
        })
    else:  # 获取内容
        LOG.info(poem)
        if cache.get(poem + 'shijing'):
            content = cache.get(poem + 'shijing')
            chapter = cache.get(poem + 'chapter')
            section = cache.get(poem + 'section')
        else:
            try:
                query = ShiJing.query.filter_by(poem=poem).first()
                content = query.content.split('。')
                chapter = query.chapter
                section = query.section
            except Exception as e:
                content = []
                chapter = section = ''
                LOG.error(e)
            cache.set(poem + 'shijing', content)
            cache.set(poem + 'chapter', chapter)
            cache.set(poem + 'section', section)
        return jsonify({
            'code': 200,
            'content': content,
            'chapter': chapter,
            'section': section,
        })


@poem.route('/introduction/', methods=['GET'])
def get_introduction():
    """
    诗人简介
    """
    param = request.args
    poet = param.get('poet')
    dynasty = param.get('dynasty')
    introduction = cache.get(poet + dynasty)
    if not introduction:
        try:
            item = PoetIntroduction.query.filter_by(dynasty=dynasty, poet=poet).first()
            code = 200
            introduction = item.descb
            cache.set(poet + dynasty, introduction)
        except Exception as e:
            LOG.error("Get Introduction Error {}".format(e))
            introduction = 'error'
            code = 404
    else:
        code = 200
    return jsonify({'code': code, 'introduction': introduction})
