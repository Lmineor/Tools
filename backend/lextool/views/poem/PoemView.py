from functools import wraps
import json
import re

from flask import Blueprint
from flask import request
from flask import jsonify

from ...models.poem import *
from ...cache import cache
from ...config.default import DefaultConfig
from ...logger import logger
from ...utils.simp2tra import simp2tra


poem = Blueprint('poem', __name__)


def check_param(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        param = request.args
        page = param.get('page')
        limits = param.get('limits')
        try:
            if page:
                int(page)
            if limits:
                int(limits)
        except ValueError:
            return jsonify({'msg': 'Params error'})
        else:
            return f(*args, **kwargs)

    return decorated


@poem.route('/poets/', methods=['GET'])
@check_param
def get_author():
    """
    得到某个朝代的作者列表
    """
    param = request.args
    dynasty = param.get('dynasty')
    page = int(param.get('page', 0))
    limits = int(param.get('limits', 0))
    logger.info("Get Poets of {} in page {}".format(dynasty, page))
    if cache.get('__poets' + dynasty + str(page) + str(limits)):
        data = json.loads(cache.get('__poets' + dynasty + str(page)))
        total = data['total']
        poets = data['poets']
        logger.info("Get Poets of {} in page {} by cache".format(dynasty, page))
        code = 200
    else:
        try:
            paginate_obj = PoetIntroduction.query.filter_by(dynasty=dynasty).paginate(
                page=page,
                per_page=limits if limits else DefaultConfig.PER_PAGE,
                error_out=False
            )
            total = paginate_obj.total
            code = 200
            poets = [item.poet for item in paginate_obj.items]
            cache.set('__poets' + dynasty + str(page) + str(limits), json.dumps({'total': total, 'poets': poets}))
        except Exception as e:
            code = 404
            poets = []
            total = 0
            logger.error("Error: {}".format(e))
    data = {
        'code': code,
        'total': total,
        'poets': poets,
        'limits': limits
    }
    return jsonify(data)


@poem.route('/poems/', methods=['GET'])
@check_param
def get_poems():
    """
    获取诗人的诗作
    """
    param = request.args
    poet = simp2tra(param.get('poet'))
    dynasty = param.get('dynasty')
    if cache.get(poet + dynasty + "poems"):
        logger.info("Get {} {}'s Poems by cache".format(dynasty, poet))
        poems = cache.get(poet + dynasty + "poems")
    else:
        try:
            logger.info("Get {} {}'s Poems".format(dynasty, poet))
            items = PoemTangSong.query.filter_by(poet=poet, dynasty=dynasty).all()
            poems = [item.poem for item in items]
            cache.set(poet + dynasty + "poems", poems)
        except Exception as e:
            poems = []
            logger.error("Error : {}".format(e))
    return jsonify({
        'code': 200,
        'poems': poems
    })


@poem.route('/search/', methods=['GET'])
@check_param
def search_poets():
    """
    获取诗人的诗作
    """
    param = request.args
    keyword = simp2tra(param.get('keyword'))
    page = param.get('page')
    logger.info("Search Poets has {}".format(keyword))
    has_cache = cache.get('/poet/search' + keyword + str(page))
    if not keyword or not isinstance(keyword, str):
        return jsonify({'code': 200, 'poets': []})
    if has_cache:
        poets = has_cache
        total = cache.get('/poet/search' + keyword + 'total')
    else:
        try:
            poets = PoetIntroduction.search_poet(keyword, page)
            total = PoetIntroduction.search_keyword_total(keyword)
            cache.set('/poet/search' + keyword + str(page), poets)
            cache.set('/poet/search' + keyword + 'total', total)
        except Exception as e:
            poets = []
            total = 0
            logger.error("Error : {}".format(e))
    return jsonify({
        'code': 200,
        'poets': poets,
        'total': total
    })


@poem.route('/content/', methods=['GET'])
@check_param
def get_content():
    """
    获取诗歌内容
    """
    param = request.args
    poet = param.get('poet')
    dynasty = param.get('dynasty')
    poem = param.get('poem')
    logger.info("Get {}'s {}'s content".format(poet, poem))
    if cache.get(poet + dynasty + poem):
        content = cache.get("content" + poet + dynasty + poem)
    else:
        try:
            item = PoemTangSong.query.\
                filter_by(
                    poet=poet,
                    dynasty=dynasty,
                    poem=poem).first()
            content = re.split("。|？", item.paragraphs) if item else []
            cache.set("content" + poet + dynasty + poem, content)
        except Exception as e:
            content = []
            logger.error("Error is: {}".format(e))
    return jsonify({
        'code': 200,
        'content': content
    })


@poem.route('/lunyu/', methods=['GET'])
@check_param
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
                logger.error(e)
            cache.set('chapters', chapters)
        return jsonify({
            'code': 200,
            'chapters': chapters
        })
    else:
        logger.info('chapter: ' + chapter)
        if cache.get('chapter'):
            paragraphs = cache.get('chapter')
        else:
            try:
                paragraphs = PoemLunyu.query.filter_by(chapter=chapter).first().paragraphs
            except Exception as e:
                paragraphs = ''
                logger.error(e)
            cache.set(chapter, paragraphs)
        return jsonify({
            'code': 200,
            'paragraphs': paragraphs.split('|')
        })


@poem.route('/songci/', methods=['GET'])
@check_param
def get_songci():
    """
    test
    """
    param = request.args
    poet = param.get('poet')
    rhythmic = param.get('rhythmic')
    page_str = param.get('page', '0')
    limits_str = param.get('limits', '0')
    page = int(page_str)
    limits = int(limits_str)
    cache_key = '__songCi' + 'page' + page_str + 'limits' + limits_str + poet + rhythmic
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
                items = CiAuthor.query.paginate(page=page, per_page=DefaultConfig.PER_PAGE, error_out=False)
                total = items.total
                cache.set('poets_num' + 'songci', total)
                poets = list(set([item.poet for item in items.items]))
            except Exception as e:
                poets = []
                logger.error(e)
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
                logger.error(e)
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
                logger.error(e)
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
        paragraphs = cache_data
    else:
        try:
            query_obj = PoemSongci.query.filter_by(poet=poet, rhythmic=rhythmic).first().paragraphs
            paragraphs = re.split('。|？', query_obj)
            cache.set(cache_key, paragraphs)
        except Exception as e:
            paragraphs = ''
            logger.error(e)
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
        logger.info("GET By Cache Req {}".format(cache_key))
        rhythmics = cache_data
    else:
        try:
            items = PoemSongci.query.filter_by(poet=poet).all()
            rhythmics = [item.rhythmic for item in items]
        except Exception as e:
            rhythmics = []
            logger.error(e)
        cache.set(cache_key, rhythmics)

    return jsonify({
            'code': 200,
            'rhythmics': rhythmics
        })


@poem.route('/songci/poets/', methods=['GET'])
@check_param
def get_songci_poets():
    """
    test
    """
    param = request.args
    page_str = param.get('page', '0')
    limits_str = param.get('limits', '0')
    page = int(page_str)
    limits = int(limits_str)

    cache_key = '__songCi: ' + 'page: ' + page_str + 'limits: ' + limits_str
    cache_data = cache.get(cache_key)
    if cache_data:
        data = json.loads(cache_data)
        total = data['total']
        poets = data['poets']
    else:
        try:
            query_obj = CiAuthor.query.paginate(
                page=page,
                per_page=limits if limits else DefaultConfig.PER_PAGE,
                error_out=False)
            total = query_obj.total
            poets = [item.poet for item in query_obj.items]
            cache_data = {'total': total, 'poets': poets}
            cache.set(cache_key, json.dumps(cache_data))
        except Exception as e:
            poets = []
            total = 0
            logger.error(e)
        cache.set(str(page) + 'songci', poets)
    return jsonify({
        'code': 200,
        'poets': poets,
        'total': total
    })


@poem.route('/shijing/', methods=['GET'])
@check_param
def get_shijing():
    """
    test
    """
    param = request.args
    poem = param.get('poem')
    page = param.get('page')
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
                items = ShiJing.query.paginate(page=page, per_page=DefaultConfig.PER_PAGE, error_out=False).items
                poems = list(set([item.poem for item in items]))
            except Exception as e:
                poems = []
                logger.error(e)
            cache.set(str(page) + 'shijing', poems)
        return jsonify({
            'code': 200,
            'poems': poems,
            'total': total
        })
    else:  # 获取内容
        logger.info(poem)
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
                logger.error(e)
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
@check_param
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
            logger.error("Get Introduction Error {}".format(e))
            introduction = 'error'
            code = 404
    else:
        code = 200
    return jsonify({'code': code, 'introduction': introduction})
