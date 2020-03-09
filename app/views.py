# -*- coding: utf-8 -*-
from flask import render_template


def init_views(app):
    # 主页，输入URL之后的页面，显示按钮《开始爬取》 《显示数据》 《清空数据》
    @app.route('/')
    def index():
        return render_template('index.html')

    # “开始爬取” 接口
    @app.route('/start_spider')
    def start_spider():
        return render_template('start_spider.html')

    # “网站首页” 接口
    @app.route('/gdut_index')
    def gdut_index():
        return render_template('gdut_index.html')

    # “清空数据” 接口
    @app.route('/clear_data')
    def clear_data():
        return render_template('clear_data.html')
