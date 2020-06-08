from ..views.poem import PoemView
from ..views.shorturl import ShortUrlView
from ..views.user import UserView
from ..views.enwords import WordsView


def register_blueprints(app):
    app.register_blueprint(PoemView.poem, url_prefix='/poem')
    app.register_blueprint(UserView.user, url_prefix='/user')
    app.register_blueprint(ShortUrlView.shorturl, url_prefix='/shorturl')
    app.register_blueprint(WordsView.words, url_prefix='/words')
