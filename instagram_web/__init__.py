from app import app
from flask import render_template
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.edits.views import edits_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from helpers import *
from models.user import User


assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(edits_blueprint, url_prefix="/users/edit")



@app.errorhandler(500) # return a response when a type of error is raised
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def not_found_error(e):
    return render_template('404.html'), 404


@app.route("/")
def home():
    all_users = User.select() # select all users
    return render_template('home.html', all_users = all_users)

