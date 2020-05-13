import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # >>> import os
    # >>> import codecs
    # >>> codecs.encode(os.urandom(16), 'hex').decode()
    # '8f7329a65d27fac7ee34d989de2cb2c0'
    SECRET_KEY = os.environ.get('SECRET_KEY') or '8f7329a65d27fac7ee34d989de2cb2c0'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    FLASK_ADMIN_SWATCH = 'simplex'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_SERVE_LOCAL = True
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN') or 'wuqingcong'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'avatars'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


class ProductionConfig(Config):
    TEST=1


class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True