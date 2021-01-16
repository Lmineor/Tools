from functools import wraps
import json
import re

from flask import (Blueprint, request, jsonify, abort)
from sqlalchemy import or_

from ...models.poem import *
from ...common.cache import cache, return_if_has_cache
from ...common.logger import LOG
from ...common.response import not_found_resp, success_resp
from ...config.config import Cfg
from ...utils.simp2tra import simp2tra
from ...common.exceptions import PoemNotFound


poem = Blueprint('poem', __name__)


def _make_cache_key(request, cache_info: dict):
    """
    request: current request
    cache_info: the info to make cache. a format of dict
    """
    cache_key = {'url': request.path}
    cache_key.update(cache_info)
    return json.dumps(cache_key)


@poem.route('/poets', methods=['GET'])
def get_poets():
    """
    获取指定朝代的所有作者，若不指定朝代，则默认返回“唐”朝的作者信息
    """
    param = request.args
    dynasty = param.get('dynasty', '唐')
    page = param.get('page', 1, type=int)
    per_page = param.get('per_page', Cfg.TOOLS.pagination, type=int)
    LOG.info("Get Poets of {} in page {}".format(dynasty, page))
    
    cache_key = _make_cache_key(
        request, {'dynasty': dynasty,'page': page,'per_page': per_page}
    )
    cache_data = cache.get(cache_key)
    
    if cache_data and not Cfg.TOOLS.debug:
        data = cache_data
        LOG.info("Get Poets of {} in page {} by cache".format(dynasty, page))
        return success_resp(data)
    else:
        paginate_obj = Poet.query.filter_by(dynasty=dynasty).paginate(
            page=page,
            per_page=per_page,
            error_out=True
        )
        if not paginate_obj.items:
            return not_found_resp({'poem': dynasty})
        data = {
            'total': paginate_obj.total,
            'poets': [item.to_dict() for item in paginate_obj.items],
            'per_page': per_page,
            'has_next': paginate_obj.has_next,
            'has_prev': paginate_obj.has_prev,
        }
        cache.set(cache_key, data)
        return success_resp(data)


@poem.route('/poems', methods=['GET'])
def get_poems():
    """
    获取诗人的诗作， 若不指定诗人，则默认返回唐-李白的诗作
    """
    param = request.args
    poet = simp2tra(param.get('poet', '李白'))
    dynasty = param.get('dynasty', '唐')
    req_info = {'poet': poet, 'dynasty': dynasty}
    
    LOG.info("Get {} {}'s Poems".format(dynasty, poet))
    cache_key = _make_cache_key(request, req_info)
    cache_data = cache.get(cache_key)
    
    if cache_data and not Cfg.TOOLS.debug:
        LOG.info("Get {} {}'s Poems by cache".format(dynasty, poet))
        poems = cache_data
        return success_resp(req_info, {'poems': poems})
    else:
        try:
            poet_obj = Poet.query.filter_by(poet=poet, dynasty=dynasty).first()
            poems = [poem.to_dict() for poem in poet_obj.poems]
            req_info.update({'poems': poems})
            cache.set(cache_key, poems)
        except Exception as e:
            LOG.error("Error : {}".format(e))
            return not_found_resp(req_info)
        return success_resp(req_info, {'poems': poems})


@poem.route('/search', methods=['GET'])
def search_poets():
    """
    获取诗人的诗作
    TODO(lex):优化代码逻辑
    """
    param = request.args
    keyword = simp2tra(param.get('keyword'))
    page = param.get('page', 1, type=int)
    LOG.info("Search Poets has {}".format(keyword))

    req_info = {'keyword': keyword, 'page': page}
    cache_key = _make_cache_key(request, req_info)
    cache_data = cache.get(cache_key)
    if not keyword or not isinstance(keyword, str):
        return jsonify({'code': 200, 'poets': []})
    if cache_data:
        data = json.loads(cache_data)
        poets = data['poets']
        total = data['total']
    else:
        try:
            poets = Poet.search_poet(keyword, page)
            total = Poet.search_keyword_total(keyword)
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

def _make_content_dict(request) -> dict:
    """
    tranfer request to dict which needed in get_content()
    """
    param = request.args
    return {
        'poet': param.get('poet'),
        'dynasty': param.get('dynasty'),
        'poem': param.get('poem')
    }

@poem.route('/content', methods=['GET'])
def get_content():
    """
    获取诗歌内容
    """    
    req_info = _make_content_dict(request)
    cache_key = _make_cache_key(request, req_info)
    LOG.info("Get {}'s {}'s content".format(poet, poem))
    
    if cache.get(cache_key):
        content = cache.get(cache_key)
        return success_resp(req_info.update({'content': content}))
    else:
        try:
            poet_obj = Poet.query.filter_by(
                    poet=poet,
                    dynasty=dynasty).first()
            content = poet_obj.poems.filter_by(poem=poem).first().to_dict()
            cache.set(cache_key, content)
        except Exception as e:
            LOG.error("Error is: {}".format(e))
            return not_found_resp(req_info)
        return success_resp(req_info, {'content': content})


def get_lunyu_chapters():
    """
    获取论语所有的章名
    """
    try:
        items = Lunyu.query.all()
        chapters = [item.to_dict(filters=['chapter', 'chapter_sim']) for item in items]
    except Exception as e:
        chapters = []
        LOG.error(e)
    return chapters


def get_lunyu_paragraphs(chapter):
    try:
        chapter_filter = {or_(Lunyu.chapter==chapter, Lunyu.chapter_sim==chapter)}
        paragraphs_data = Lunyu.query.filter(*chapter_filter).first().to_dict()
        paragraphs_data['paragraphs'] = paragraphs_data['paragraphs'].split('|')
        return paragraphs_data
    except Exception as e:
        paragraphs = ''
        LOG.error(e)
        raise Exception("Erro")
    

def _make_lunyu_dict(request) -> dict:
    param = request.args
    return {
        'chapter': param.get('chapter', None),
    }


@poem.route('/lunyu/', methods=['GET'])
def get_lunyu():
    """
    获取论语的内容
    chapter: 章
    """
    req_info = _make_lunyu_dict(request)
    cache_key = _make_cache_key(request, req_info)
    if req_info['chapter'] is None:
        # 若不指定chapter，则处理逻辑为, 获取论语的所有章，简化接口
        if cache.get(cache_key) and not Cfg.TOOLS.debug:
            resp_data = cache.get(cache_key)
            return success_resp(req_info, resp_data)
        else:
            chapters = get_lunyu_chapters()
            resp_data = {'chapters': chapters}
            cache.set(cache_key, resp_data)
            req_info.pop('chapter') # in this case, `chapter` is None, so we pop it
            return success_resp(req_info, resp_data)
    else:
        LOG.info('chapter: ' + req_info['chapter'])
        if cache.get(cache_key) and not Cfg.TOOLS.debug:
            resp_data = cache.get(cache_key)
            return success_resp(req_info, resp_data)
        else:
            paragraphs = get_lunyu_paragraphs(req_info['chapter'])
            resp_data = {'paragraphs': paragraphs}
            cache.set(cache_key, resp_data)
        return success_resp(req_info, resp_data)


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
                items = CiPoet.query.paginate(page=page, per_page=Cfg.TOOLS.pagination, error_out=False)
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
                items = Songci.query.filter_by(poet=poet).all()
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
                paragraphs = Songci.query.filter_by(poet=poet, rhythmic=rhythmic).first().paragraphs.split('。')
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
            query_obj = Songci.query.filter_by(poet=poet, rhythmic=rhythmic).first()
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
            items = Songci.query.filter_by(poet=poet).all()
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
            query_obj = CiPoet.query.paginate(
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
            item = Poet.query.filter_by(dynasty=dynasty, poet=poet).first()
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
