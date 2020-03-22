import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '\x03d\xf4\x95J\x15\xa4B\xfb\xc0\xaf \xd1A[j$}\x18\x16a\xe7\xd0\xec'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    BABEL_DEFAULT_LOCALE = 'zh'

    @staticmethod
    def init_app(app):
        pass




class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:a1234567890!@127.0.0.1:3306/gdutnews'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

config = {
    'default': DevelopmentConfig
}

# GDUT的一些通用变量
class PublicGdutWebVar:
    url_pre = 'http://gdutnews.gdut.edu.cn/'