from ..views.poem import PoemView
from ..views.dwz import DwzView
from ..views.user import UserView
from ..views.enwords import WordsView


def register_blueprints(app):
    app.register_blueprint(PoemView.poem, url_prefix='/poem')
    app.register_blueprint(UserView.user, url_prefix='/user')
    app.register_blueprint(DwzView.dwz, url_prefix='/dwz')
    app.register_blueprint(WordsView.words, url_prefix='/words')
