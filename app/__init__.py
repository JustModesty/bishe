# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from .views import init_views

bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)

    # 这一句方便开发
    # app.config['DEBUG'] = True

    # 使用Bootstrap
    bootstrap.init_app(app)

    # 使用菜单
    # nav = Nav()

    # nav.register_element('top', Navbar(u'广东工业大学新闻网',View(u'主页', 'index')))
    # nav.init_app(app)

    init_views(app)
    return app
