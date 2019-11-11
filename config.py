import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'yoyoyoyyoyoyo')
    NO_OF_PLACEHOLDER_IMAGES = 30
    AVG_READING_SPEED = 310
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    MONGODB_SETTINGS = {
        'db': 'resume',
        'host' : 'mongodb://localhost/resume'
    }
    
    POSTS_PER_PAGE = 5
    S3_BUCKET = 'resume-website-flask'
    PROJECT_ROOT = 'static'
    IMAGE_SIZES = [1, (600,0), (200,200), (1024,1024)]
    IMAGE_SIZE_FORMAT = ["full", "post", "small_thumb", "big_thumb"]
    IMAGE_QUALITY = 95
