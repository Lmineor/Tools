from backend.Tools.views.poem import PoemView
from backend.Tools.views.user import UserView
from backend.Tools.views.shorturl import ShortUrlView



def register_blueprints(app):
	app.register_blueprint(PoemView.poem, url_prefix='/poem')
	app.register_blueprint(UserView.user, url_prefix='/user')
	app.register_blueprint(ShortUrlView.shorturl, url_prefix='/shorturl')
