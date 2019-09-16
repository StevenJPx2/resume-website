from flask import Flask
from flask_bootstrap import Bootstrap
from flaskext.markdown import Markdown
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
md = Markdown(app)


from app import routes