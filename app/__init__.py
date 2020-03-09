# -*- coding: utf-8 -*-
from os import path

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config


basedir = path.abspath(path.dirname(__file__))

db = SQLAlchemy()

bootstrap = Bootstrap()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    # 这一句方便开发
    # app.config['DEBUG'] = True

    # 使用Bootstrap
    bootstrap.init_app(app)

    # 使用菜单
    # nav = Nav()

    # nav.register_element('top', Navbar(u'广东工业大学新闻网',View(u'主页', 'index')))
    # nav.init_app(app)
    # from .auth import auth as auth_blueprint
    from .main import main_handler as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
