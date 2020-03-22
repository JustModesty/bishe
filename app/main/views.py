from flask import render_template
from lxml import etree

from app import db
from . import main_handler
import requests
from app.models import *
from config import PublicGdutWebVar


@main_handler.route('/')
def index():
    return render_template('index.html')


# “开始爬取” 接口
@main_handler.route('/start_spider')
def start_spider():
    response = requests.get('http://gdutnews.gdut.edu.cn/')
    content = response.content
    content = content.decode('utf-8')
    html = etree.HTML(content)
    # 抓取banner
    banner = html.xpath('//div[@class="banner"]/img/@src')[0]
    print(banner)
    # 存取数据库
    banner_url = PublicGdutWebVar.url_pre + banner
    banner = BannerTbl(banner_image=banner_url)
    db.session.add(banner)
    db.session.commit()

    return render_template('start_spider.html')


# “网站首页” 接口
@main_handler.route('/gdut_index')
def gdut_index():
    # banner
    banner_query = BannerTbl.query.first()
    banner_site = banner_query.banner_image

    return render_template('gdut_index.html', banner_site=banner_site)


# “清空数据” 接口
@main_handler.route('/clear_data')
def clear_data():
    # 删除banner
    BannerTbl.query.delete()
    return render_template('clear_data.html')
