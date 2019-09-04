import os
from config import *
from flask import Flask
from models.base_model import db
from models.user import User

#for CFRS protection
from flask_wtf.csrf import CSRFProtect

# for login manager
from flask_login import LoginManager


web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'instagram_web')

app = Flask('NEXTAGRAM', root_path=web_dir)


if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")


csrf = CSRFProtect(app)

# for login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get_or_none(User.id==user_id)

#for Google login
from authlib.flask.client import OAuth

oauth = OAuth()

oauth.register('google',
    client_id=Config.client_id,
    client_secret=Config.client_secret,

    # exchange a temporary token for an access_token
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    
    #where user is taken to for Google login
    authorize_url='https://accounts.google.com/o/oauth2/auth',

    #the beginning part of URL used for retreiving user information like name, email after succesfuly authentication
    api_base_url='https://www.googleapis.com/oauth2/v1/',

    client_kwargs={
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'token_endpoint_auth_method': 'client_secret_basic',
        'token_placement': 'header',
        'prompt': 'consent'
    }
)

oauth.init_app(app)

@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc
