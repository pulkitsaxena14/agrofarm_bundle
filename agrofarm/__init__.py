from flask import Flask, render_template, request

from agrofarm.admin.controllers import admin
#from agrofarm.cache import cache
from agrofarm.config import configure_app
from agrofarm.data.models import db
#from flask import abort, Flask, g, render_template, request
#from flask_babel import Babel
#from flask_security import current_user
#from bookshelf.utils import get_instance_folder_path
from agrofarm.main.controllers import main

app = Flask(__name__,
            # instance_path=get_instance_folder_path(),
            instance_relative_config=True,
            template_folder='templates')

#babel = Babel(app)
configure_app(app)
# cache.init_app(app)
db.init_app(app)
# app.jinja_env.add_extension('jinja2.ext.loopcontrols')
# @app.url_defaults
# def set_language_code(endpoint, values):
#    if 'lang_code' in values or not g.get('lang_code', None):
#        return
#    if app.url_map.is_endpoint_expecting(endpoint, 'lang_code'):
#        values['lang_code'] = g.lang_code

# @app.url_value_preprocessor
# def get_lang_code(endpoint, values):
#    if values is not None:
#        g.lang_code = values.pop('lang_code', None)

# @app.before_request
# def ensure_lang_support():
#    lang_code = g.get('lang_code', None)
#    if lang_code and lang_code not in app.config['SUPPORTED_LANGUAGES'].keys():
#        return abort(404)

# @babel.localeselector
# def get_locale():
#    return g.get('lang_code', app.config['BABEL_DEFAULT_LOCALE'])

# @babel.timezoneselector
# def get_timezone():
#    user = g.get('user', None)
#    if user is not None:
#        return user.timezone


@app.errorhandler(400)
def bad_requert_error(error):
    app.logger.error('Bad Request: %s', (request.path, error))
    return render_template('400.html'), 400


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('Page not found: %s', (request.path, error))
    return render_template('404.html'), 404


@app.errorhandler(405)
def method_not_allowed(error):
    app.logger.error('Method Not Allowed: %s', (request.path, error))
    return render_template('405.html'), 405


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('500.html'), 500


@app.errorhandler(Exception)
def unhandled_exception(error):
    app.logger.error('Unhandled Exception: %s', (error))
    return render_template('500.html'), 500

# @app.context_processor
# def inject_data():
#    return dict(user=current_user, \
#        lang_code=g.get('lang_code', None))

# @app.route('/')
# @app.route('/<lang_code>/')
# @cache.cached(300)
# def home():
#    return render_template('home.html')


app.register_blueprint(main, url_prefix='/')
#app.register_blueprint(main, url_prefix='/<lang_code>/main')
app.register_blueprint(admin, url_prefix='/admin')
#app.register_blueprint(admin, url_prefix='/<lang_code>/admin')
