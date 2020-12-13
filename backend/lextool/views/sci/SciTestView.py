import requests

from flask import Blueprint, request
from flask import jsonify

from ...common.logger import LOG

sci = Blueprint('sci', __name__)


@sci.route("/test", methods=['POST'])
def test_sci():
    url = request.get_json()['url']
    LOG.info("Run a {} test of sci".format(url))
    try:
        response = requests.request('GET', url, timeout=5000)
        times = int(response.elapsed.total_seconds()*1000)
        code = 200
    except Exception as e:
        LOG.error(e)
        times = -1
        code = 403
    return jsonify({'code': code, 'times': times})
