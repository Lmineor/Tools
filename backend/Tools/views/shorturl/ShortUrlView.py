from flask import request
from flask import redirect
from flask import Blueprint
from flask import jsonify
from flask import render_template

from backend.Tools.logger import logger
from backend.Tools.models.shorturl import ShortUrl
from backend.Tools.models import db
from backend.Tools.utils.gen_dwz import gen_dwz


shorturl = Blueprint('shorturl', __name__)


@shorturl.route('/OriginUrl', methods=['POST'])
def get_originurl():
    """
    短链还原部分
    """
    shorturl = request.get_json()['shorturl']
    if not shorturl:
        return None
    try:
        item = ShortUrl.query.filter(ShortUrl.short_url == shorturl).first()
        origin_url = item.origin_url
    except Exception as e:
        origin_url = '生成失败,该短链不存在'
        logger.error(e)
    return jsonify({
        'code': 200,
        'OriginUrl': origin_url
    })


@shorturl.route('/shorten', methods=['POST'])
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
        shortU = ShortUrl(origin_url=url)
        db.session.add(shortU)
        db.session.flush()
        urlid = shortU.id  # 得到最后一调数据插入的id
        su = gen_dwz(urlid)  # 生成短链
        logger.info("短链成功生成")
        shortU.short_url = su
        db.session.add(shortU)
        db.session.flush()
        db.session.commit()
    except Exception as e:
        logger.error(e)
    if not su:
        item = ShortUrl.query.filter(ShortUrl.origin_url == url).first()
        if item:
            su = item.short_url
    data = {
        'code': 200,
        'url': su
    }
    return jsonify(data)


def __pre_get(url):
    su = ''
    try:
        item = ShortUrl.query.filter(ShortUrl.origin_url == url).first()
        if item:
            su = item.short_url
    except Exception as e:
        logger.error(e)
    return su


@shorturl.route('/s/<code>', methods=['GET'])
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
