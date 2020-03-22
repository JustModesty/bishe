from flask import render_template
from lxml import etree

from app import db
from . import main_handler
import requests
from app.models import *
from config import PublicGdutWebVar

# from sqlalchemy import create_engine
# # DB_CONNECT = 'mysql+mysqlconnector://root:a1234567890!@127.0.0.1:3306/gdutnews?charset=utf8'
# DB_CONNECT = 'mysql+pymysql://root:a1234567890!@127.0.0.1:3306/gdutnews'
# engine = create_engine(DB_CONNECT, echo=False, pool_size=10, pool_recycle=3600)
# conn = engine.connect()

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:a1234567890!@127.0.0.1:3306/gdutnews", max_overflow=0, pool_size=5)
Session = sessionmaker(bind=engine)


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
    # 存取数据库
    banner_url = PublicGdutWebVar.url_pre + banner
    banner = BannerTbl(banner_image=banner_url)
    db.session.add(banner)
    db.session.commit()

    # 抓取Menu
    menu_link_list = html.xpath('//div[@class="menu"]/ul/li/a/@href')
    menu_name_list = html.xpath('//div[@class="menu"]/ul/li/a/text()')
    # 存入数据库
    for i in range(len(menu_link_list)):
        link = menu_link_list[i]
        name = menu_name_list[i]
        if link.startswith('http'):
            pass
        else:
            link = PublicGdutWebVar.url_pre + link
        menu = MenuTbl(menu_href=link, menu_name=name)
        db.session.add(menu)
        db.session.commit()
    # 抓取topnews
    topnews_title = html.xpath('//div[@class="topnewsc"]//h1/a/text()')[0]
    topnews_link = html.xpath('//div[@class="topnewsc"]//h1/a/@href')[0]
    # 存入数据库
    topnews_link = PublicGdutWebVar.url_pre + topnews_link
    topnews = TopnewsTbl(topnews_title=topnews_title, topnews_href=topnews_link)
    db.session.add(topnews)
    db.session.commit()

    return render_template('start_spider.html')


# “网站首页” 接口
@main_handler.route('/gdut_index')
def gdut_index():
    # banner
    session = Session()
    cursor = session.execute('select count(*) from banner_tbl')
    session.commit()
    values = cursor.fetchall()

    if values[0][0] > 0:
        # banner
        banner_query = BannerTbl.query.first()
        banner_site = banner_query.banner_image
        # menu
        menu_query = MenuTbl.query.all()
        # topnews
        topnews_query = TopnewsTbl.query.first()
        topnews_href = topnews_query.topnews_href
        topnews_title = topnews_query.topnews_title

        return render_template('gdut_index.html', banner_site=banner_site, menu_query=menu_query, topnews_href=topnews_href,topnews_title=topnews_title)
    else:
        return render_template('gdut_index.html')


# “清空数据” 接口
@main_handler.route('/clear_data')
def clear_data():
    # 删除banner
    session = Session()
    session.execute('delete from banner_tbl where 1=1')
    session.execute('delete from menu_tbl where 1=1')
    session.execute('delete from topnews_tbl where 1=1')
    session.commit()
    return render_template('clear_data.html')
