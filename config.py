import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'yoyoyoyyoyoyo')
    UNSPLASH_ACCESS_KEY = '46fa2b12c274d628d2958c67bcbf9cbc8ca3221c3def10e004580023efa40ea3'
    NO_OF_PLACEHOLDER_IMAGES = 30
    AVG_READING_SPEED = 310
    MONGO_DBNAME = 'restdb'
    MONGO_URI = 'mongodb://localhost:27017/restdb'