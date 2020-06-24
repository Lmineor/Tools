from flask import Blueprint
from flask import request
from flask import jsonify
from sqlalchemy.sql.expression import func

from ...models.poem import *
from ...cache import cache
from ...config.default import DefaultConfig
from ...logger import logger
from ...utils.simp2tra import simp2tra


poem = Blueprint('poem', __name__)


@poem.route('/poet/poets', methods=['POST'])
def get_author():
    """
    得到某个朝代的作者列表
    """
    dynasty = request.get_json()['dynasty']
    page = request.get_json()['page']
    logger.info("Get Poets of {} in page {}".format(dynasty, page))
    if cache.get(str(page) + dynasty):
        total = cache.get('poets_num' + dynasty)
        poets = cache.get(str(page) + dynasty)
        code = 200
    else:
        try:
            total = db.session.query(func.count(PoetIntroduction.id)).filter(PoetIntroduction.dynasty == dynasty).scalar()
            items = PoetIntroduction.query.filter_by(dynasty=dynasty).paginate(
                page=page, per_page=DefaultConfig.PER_PAGE, error_out=False).items
            code = 200
            poets = list(set([item.poet for item in items]))
            cache.set('poets_num' + dynasty, total)
            cache.set(str(page) + dynasty, poets)
        except Exception as e:
            code = 404
            poets = []
            total = 0
            logger.error("Error: {}".format(e))
    data = {
        'code': code,
        'total': total,
        'poets': poets
    }
    return jsonify(data)


@poem.route('/poet/poems', methods=['POST'])
def get_poems():
    """
    获取诗人的诗作
    """
    poet = request.get_json()['poet']
    dynasty = request.get_json()['dynasty']
    logger.info("Get {} {}'s Poems".format(dynasty, poet))
    if cache.get(poet + dynasty + "poems"):
        poems = cache.get(poet + dynasty + "poems")
    else:
        try:
            items = db.session.query(PoemTangSong.poem).filter(
                PoemTangSong.poet == poet, PoemTangSong.dynasty == dynasty).all()
            poems = [item[0] for item in items]
            cache.set(poet + dynasty + "poems", poems)
        except Exception as e:
            poems = []
            logger.error("Error : {}".format(e))
    return jsonify({
        'code': 200,
        'poems': poems
    })


@poem.route('/poet/content', methods=['POST'])
def get_content():
    """
    获取诗歌内容
    """
    poet = request.get_json()['poet']
    dynasty = request.get_json()['dynasty']
    poem = request.get_json()['poem']
    logger.info("Get {}'s {}'s content".format(poet, poem))
    if cache.get(poet + dynasty + poem):
        content = cache.get("content" + poet + dynasty + poem)
    else:
        try:
            content = db.session.query(PoemTangSong).filter(PoemTangSong.poet == poet,
                                                            PoemTangSong.dynasty == dynasty,
                                                            PoemTangSong.poem == poem).first().paragraphs
            content = content.split('。')
            # content = PoemTangSong.query.filter_by(poet=poet, dynasty=dynasty, poem=poem).first().paragraphs
            cache.set("content" + poet + dynasty + poem, content)
        except Exception as e:
            content = []
            logger.error("Error is: {}".format(e))
    return jsonify({
        'code': 200,
        'content': content
    })


@poem.route('/lunyu', methods=['POST', 'GET'])
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
        chapter = request.get_json()['chapter']
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


@poem.route('/songci', methods=['POST', 'GET'])
def get_songci():
    """
    test
    """
    author = request.get_json()['author']
    rhythmic = request.get_json()['rhythmic']
    page = request.get_json()['page']
    if page:  # 获取作者翻页数据
        if cache.get('authors_num' + 'songci'):
            total = int(cache.get('authors_num' + 'songci'))
        else:
            total = len(CiAuthor.query.all())
            cache.set('authors_num' + 'songci', total)
        if cache.get(str(page) + 'songci'):
            authors = cache.get(str(page) + 'songci')
        else:
            try:
                items = CiAuthor.query.paginate(page=page, per_page=DefaultConfig.PER_PAGE, error_out=False).items
                authors = list(set([item.name for item in items]))
            except Exception as e:
                authors = []
                logger.error(e)
            cache.set(str(page) + 'songci', authors)
        return jsonify({
            'code': 200,
            'authors': authors,
            'total': total
        })
    elif not rhythmic:  # 获取词牌名s
        if cache.get(author + '_ci'):
            rhythmics = cache.get(author + '_ci')
        else:
            try:
                items = PoemSongci.query.filter_by(author=author).all()
                rhythmics = list(set([item.rhythmic for item in items]))
            except Exception as e:
                rhythmics = []
                logger.error(e)
            cache.set(author + '_ci', rhythmics)
        return jsonify({
            'code': 200,
            'rhythmics': rhythmics
        })
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
        return jsonify({
            'code': 200,
            'paragraphs': paragraphs
        })


@poem.route('/shijing', methods=['POST'])
def get_shijing():
    """
    test
    """
    title = request.get_json()['title']
    page = request.get_json()['page']
    if page:  # 获取诗名翻页数据
        if cache.get('title_num' + 'shijing'):
            total = int(cache.get('title_num' + 'shijing'))
        else:
            total = len(ShiJing.query.all())
            cache.set('title_num' + 'shijing', total)
        if cache.get(str(page) + 'shijing'):
            titles = cache.get(str(page) + 'shijing')
        else:
            try:
                items = ShiJing.query.paginate(page=page, per_page=DefaultConfig.PER_PAGE, error_out=False).items
                titles = list(set([item.title for item in items]))
            except Exception as e:
                titles = []
                logger.error(e)
            cache.set(str(page) + 'shijing', titles)
        return jsonify({
            'code': 200,
            'titles': titles,
            'total': total
        })
    else:  # 获取内容
        logger.info(title)
        if cache.get(title + 'shijing'):
            content = cache.get(title + 'shijing')
            chapter = cache.get(title + 'chapter')
            section = cache.get(title + 'section')
        else:
            try:
                query = ShiJing.query.filter_by(title=title).first()
                content = query.content.split('。')
                chapter = query.chapter
                section = query.section
            except Exception as e:
                content = []
                chapter = section = ''
                logger.error(e)
            cache.set(title + 'shijing', content)
            cache.set(title + 'chapter', chapter)
            cache.set(title + 'section', section)
        return jsonify({
            'code': 200,
            'content': content,
            'chapter': chapter,
            'section': section,
        })


@poem.route('/poet/introduction', methods=['POST'])
def get_introduction():
    """
    诗人简介
    """
    poet = request.get_json()['poet']
    dynasty = request.get_json()['dynasty']
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
