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


# class TestingConfig(Config):
#     TESTING = True
#     SERVER_NAME = 'localhost:5000'
#     SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
#                               'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
#     WTF_CSRF_ENABLED = False
#
#
# class Production(Config):
#     DEBUG = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
#                               'postgresql://ray:?@localhost/blog-db'


config = {
    'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    # 'production': Production,
    'default': DevelopmentConfig
}
