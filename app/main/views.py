from flask import render_template
from . import main_handler


@main_handler.route('/')
def index():
    return render_template('index.html')


# “开始爬取” 接口
@main_handler.route('/start_spider')
def start_spider():
    return render_template('start_spider.html')


# “网站首页” 接口
@main_handler.route('/gdut_index')
def gdut_index():
    return render_template('gdut_index.html')


# “清空数据” 接口
@main_handler.route('/clear_data')
def clear_data():
    return render_template('clear_data.html')
