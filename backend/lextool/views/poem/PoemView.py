from functools import wraps
import json
import re

from flask import (Blueprint, request, jsonify, abort)
from sqlalchemy import or_, and_

from ...models.poem import *
from ...common.cache import cache, return_if_has_cache
from ...common.logger import LOG
from ...common.response import not_found_resp, success_resp
from ...config.config import Cfg
from ...utils.simp2tra import simp2tra
from ...common.exceptions import PoemNotFound, FiltersTypeError


poem = Blueprint('poem', __name__)


def _make_cache_key(request, req_info: dict):
    """
    make cache key
    :param request: current wsgi request
    :param req_info: the info to make cache. depends on each models
    :return: json.dumps()
    """
    cache_key = {'url': request.path}
    cache_key.update(req_info)
    return json.dumps(cache_key)


def _make_poets_dict(request):
    param = request.args
    return {
        'dynasty': param.get('dynasty', '唐'),
        'page': param.get('page', 1, type=int),
        'per_page': param.get('per_page', Cfg.TOOLS.pagination, type=int)
    }

@poem.route('/poets', methods=['GET'])
def get_poets():
    """
    获取指定朝代的所有作者，若不指定朝代，则默认返回“唐”朝的作者信息
    """
    req_info = _make_poets_dict(request)
    LOG.info("Get Poets of {dynasty} in page {page}, as per page {per_page}".format(**req_info))
    
    cache_key = _make_cache_key(request, req_info)
    cache_data = cache.get(cache_key)
    
    if cache_data and not Cfg.TOOLS.debug:
        data = cache_data
        LOG.info("Get Poets of {} in page {} by cache".format(req_info['dynasty'], req_info['page']))
        return success_resp(data)
    else:
        try:
            filters = or_(
                Poet.dynasty_sim == req_info['dynasty'],
                Poet.dynasty == req_info['dynasty']
                )
            paginate_obj = Poet.query.filter(filters).paginate(
                page=req_info['page'],
                per_page=req_info['per_page'],
                error_out=True
            )
            if not paginate_obj.items:
                return not_found_resp(req_info)
            
            data = {
                'total': paginate_obj.total,
                'poets': [item.poet for item in paginate_obj.items],
                'per_page': req_info['per_page'],
                'has_next': paginate_obj.has_next,
                'has_prev': paginate_obj.has_prev,
            }
            
            cache.set(cache_key, data)
            return success_resp(req_info, data)
        except Exception as e:
            LOG.error(e)
            resp_data = {'msg': 'error'}
            return not_found_resp(resp_data)


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


@poem.route('/lunyu', methods=['GET'])
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


def _make_songci_req_info(request, filters=None) -> dict:
    """
    make songci request info dict
    :param request: wsgi request
    :param filters: list, for what you need when use this func
    :return: 
    """
    param = request.args
    if filters is None:
        return {
            'poet': param.get('poet'),
            'rhythmic': param.get('rhythmic'),
            'page': param.get('page', 1, type=int),
            'limits': param.get('limits', 0, type=int)
            }
    else:
        if not isinstance(filters, list):
            raise FiltersTypeError()
        return {key: param.get(key) for key in filters}

@poem.route('/songci/content', methods=['GET'])
def get_songci_content():
    """
    获取宋词的内容
    param
    poet: must
    rhythmic: must   
    """
    req_info = _make_songci_req_info(request, filters=['poet', 'rhythmic'])
    cache_key = _make_cache_key(request, req_info)
    cache_data = cache.get(cache_key)
    if cache_data and not Cfg.TOOLS.debug:
        LOG.info("GET SongCi Content By Cache")
        resp_data = cache_data
        return success_resp(req_info, resp_data)
    else:
        try:
            ci_poet_filter = {or_(CiPoet.poet == req_info['poet'], CiPoet.poet_sim == req_info['poet'])}
            ci_poem_filter = or_(Songci.rhythmic == req_info['rhythmic'], Songci.rhythmic_sim == req_info['rhythmic'])
            poet_obj = CiPoet.query.filter(*ci_poet_filter).first()
            poem_dict = poet_obj.ci.filter(ci_poem_filter).first().to_dict()
            poem_dict['paragraphs'] = re.split('。|？', poem_dict['paragraphs'])
            poem_dict['paragraphs_sim'] = re.split('。|？', poem_dict['paragraphs_sim'])
            resp_data = poem_dict
            cache.set(cache_key, resp_data)
            return success_resp(req_info, resp_data)
        except Exception as e:
            paragraphs = ''
            LOG.error(e)
            return not_found_resp(req_info)


@poem.route('/songci/poet/poems', methods=['GET'])
def get_songci_poem():
    """
    获取作者名下的所有词
    param:
    poet: must
    """
    req_info = _make_songci_req_info(request, filters=['poet'])
    cache_key = _make_cache_key(request, req_info)
    cache_data = cache.get(cache_key)
    if cache_data and not Cfg.TOOLS.debug:
        LOG.info("GET By Cache Req {}".format(cache_key))
        return success_resp(req_info, cache_data)
    else:
        try:
            filter = or_(CiPoet.poet==req_info['poet'], CiPoet.poet_sim==req_info['poet'])
            ci_poet_obj = CiPoet.query.filter(filter).first()
            rhythmics = list(set(ci.rhythmic for ci in ci_poet_obj.ci))
            resp_data = {'rhythmics': rhythmics}
            cache.set(cache_key, resp_data)
        except Exception as e:
            LOG.error(e)
            return not_found_resp(req_info)
        return success_resp(req_info, resp_data)


@poem.route('/songci/poets', methods=['GET'])
def get_songci_poets():
    """
    获取宋词的所有作者
    """
    req_info = _make_songci_req_info(request, filters=['limits', 'page'])
    cache_key = _make_cache_key(request, req_info)
    
    LOG.info("GET {}".format(cache_key))
    
    cache_data = cache.get(cache_key)
    if cache_data and not Cfg.TOOLS.debug:
        return success_resp(cache_data)
    else:
        try:
            query_obj = CiPoet.query.paginate(
                page=req_info['page'],
                per_page=req_info['limits'] if req_info['limits'] else Cfg.TOOLS.pagination,
                error_out=False)
            total = query_obj.total
            poets = [item.to_dict(filters=['poet', 'poet_sim']) for item in query_obj.items]
            resp_data = {'total': total, 'poets': poets}
            
            cache.set(cache_key, resp_data)
            
            req_info['limits'] = req_info['limits'] if req_info['limits'] else Cfg.TOOLS.pagination
            req_info['page'] = req_info['page'] if req_info['page'] else 1
            
            return success_resp(req_info, resp_data)
        
        except Exception as e:
            poets = []
            total = 0
            return not_found_resp(req_info)


@poem.route('/shijing', methods=['GET'])
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


def _make_intro_dict(request):
    """
    make poet's introduction dict
    :param request: wsgi request
    :return: dict
    """
    param = request.args
    return {
        'poet': param.get('poet', '李白'),
        'dynasty': param.get('dynasty', '唐')
    }


@poem.route('/introduction', methods=['GET'])
def get_introduction():
    """
    诗人简介
    """
    req_info = _make_intro_dict(request)
    cache_key = _make_cache_key(request, req_info)
    cache_data = cache.get(cache_key)
    if cache_data and not Cfg.TOOLS.debug:
        return success_resp(req_info, cache_data)
    else:
        try:
            filters = and_(
                or_(Poet.dynasty == req_info['dynasty'], Poet.dynasty_sim == req_info['dynasty']),
                or_(Poet.poet == req_info['poet'], Poet.poet_sim == req_info['poet'])
            )
            poet_obj = Poet.query.filter(filters).first()
            resp_data = poet_obj.to_dict()
            
            cache.set(cache_key, resp_data)
            
            return success_resp(req_info, resp_data)
        except Exception as e:
            LOG.error("Get Introduction Error {}".format(e))
            resp_data = {'msg': 'error'}
            return not_found_resp(resp_data)
