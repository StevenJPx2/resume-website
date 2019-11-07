from flask import Flask
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_moment import Moment
from config import Config
import wtforms_json

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
md = Markdown(app)
db = MongoEngine(app)
moment = Moment(app)
login = LoginManager(app)
login.login_view = 'admin_login'
wtforms_json.init()

from app import routes, models, errors, bucket, utils