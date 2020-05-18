# 和诗词歌赋相关的接口

from flask import Blueprint
from flask import request


poem = Blueprint('poem', __name__)

@poem.route('/getauthor', methods=['POST'])
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
    return jsonify(data)


@poem.route('/gettitle', methods=['POST'])
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
    return jsonify({
        'code': 200,
        'titles': titles
    })


@poem.route('/getpoem', methods=['POST'])
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
    return jsonify({
        'code': 200,
        'poem': poem
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
                print(items[0])
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
                paragraphs = PoemLunyu.query.filter_by(chapter = chapter).first().paragraphs
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
        return jsonify({
            'code': 200,
            'authors': authors,
            'total': total
        })
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
    if page: # 获取诗名翻页数据
        if cache.get('title_num' + 'shijing'):
            total = int(cache.get('title_num' + 'shijing'))
        else:
            total = len(ShiJing.query.all())
            cache.set('title_num' + 'shijing', total)
        if cache.get(str(page) + 'shijing'):
            titles =  cache.get(str(page) + 'shijing')
        else:
            try:
                items = ShiJing.query.paginate(page=page, per_page=PER_PAGE, error_out=False).items
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
    else: # 获取内容
        logger.info(title)
        if cache.get(title + 'shijing'):
            content = cache.get(title + 'shijing')
            chaper = cache.get(title + 'chaper')
            section = cache.get(title + 'section')
        else:
            try:
                query = ShiJing.query.filter_by(title = title).first()
                content = query.content.split('。')
                chapter = query.chapter
                section = query.section
            except Exception as e:
                content = []
                chaper = section = ''
                logger.error(e)
            cache.set(title + 'shijing', content)
            cache.set(title + 'chaper', chapter)
            cache.set(title + 'section', section)
        return jsonify({
            'code': 200,
            'content': content,
            'chapter': chapter,
            'section': section,
        })