from flask import Flask
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown
from flask_pymongo import PyMongo
from flask_moment import Moment
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
md = Markdown(app)
mongo = PyMongo(app)
moment = Moment(app)


from app import routes, models