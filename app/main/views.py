from flask import render_template
from lxml import etree

from app import db
from . import main_handler
import requests
from app.models import *
from config import PublicGdutWebVar

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
    topnews_link = PublicGdutWebVar.url_pre + html.xpath('//div[@class="topnewsc"]//h1/a/@href')[0]
    # 存入数据库
    topnews = TopnewsTbl(topnews_title=topnews_title, topnews_href=topnews_link)
    db.session.add(topnews)
    db.session.commit()

    # 抓取shcoolnews
    schoolnews_parent_href = PublicGdutWebVar.url_pre + html.xpath('//div[@class="tabcenh"]/span/a/@href')[0]
    schoolnews_parent_title = html.xpath('//div[@class="tabcenh"]/span/a/text()')[0]

    schoolnews_head_news_image = PublicGdutWebVar.url_pre + html.xpath('//div[@class="ywtop2"]/div/a/img/@src')[0]
    schoolnews_head_news_href = html.xpath('//div[@class="ywtop2"]/div/a/@href')[0]
    schoolnews_head_news_title = html.xpath('//div[@class="ywtop2"]//h3/a/text()')[0]

    # 存入数据库
    schoolnews = SchoolnewsTbl(schoolnews_parent_href=schoolnews_parent_href,
                               schoolnews_parent_title=schoolnews_parent_title,
                               schoolnews_head_news_image=schoolnews_head_news_image,
                               schoolnews_head_news_href=schoolnews_head_news_href,
                               schoolnews_head_news_title=schoolnews_head_news_title)
    db.session.add(schoolnews)
    db.session.commit()

    # 注意这是包含12个元素的列表
    schoolnews_sub_news_href = html.xpath('//div[@class="ywcon"]/ul[@class="ywul"]/li/a/@href')
    # 注意这是包含12个元素的列表
    schoolnews_sub_news_title = html.xpath('//div[@class="ywcon"]/ul[@class="ywul"]/li/a/text()')

    for i in range(len(schoolnews_sub_news_href)):
        link = schoolnews_sub_news_href[i]
        title = schoolnews_sub_news_title[i]
        schoolnewssubnews = SchoolnewssubnewsTbl(schoolnews_sub_news_href=link, schoolnews_sub_news_title=title)
        db.session.add(schoolnewssubnews)
        db.session.commit()

    # 抓取schoolnewssliding
    # 包含5个元素的列表
    schoolnews_head_news_image = html.xpath('//div[@class="main1right"]//div[@class="pages"]/ul/li/a/img/@src')
    # 包含5个元素的列表
    schoolnews_head_news_href = html.xpath('//div[@class="main1right"]//div[@class="pages"]/ul/li/a/@href')
    # 包含5个元素的列表
    schoolnews_head_news_title = html.xpath('//div[@class="main1right"]//div[@class="pages"]/ul/li/a/@title')

    for i in range(len(schoolnews_head_news_title)):
        link = PublicGdutWebVar.url_pre + schoolnews_head_news_href[i]
        title = schoolnews_head_news_title[i]
        image = PublicGdutWebVar.url_pre + schoolnews_head_news_image[i]
        row = SchoolnewsslidingTbl(schoolnews_head_news_image=image,
                                   schoolnews_head_news_href=link,
                                   schoolnews_head_news_title=title)
        db.session.add(row)
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
        # shcoolnews
        schoolnews_query = SchoolnewsTbl.query.first()
        schoolnews_parent_href = schoolnews_query.schoolnews_parent_href
        schoolnews_parent_title = schoolnews_query.schoolnews_parent_title
        schoolnews_head_news_image = schoolnews_query.schoolnews_head_news_image
        schoolnews_head_news_href = schoolnews_query.schoolnews_head_news_href
        schoolnews_head_news_title = schoolnews_query.schoolnews_head_news_title
        # schoolnewssubnews
        schoolnewssubnews_query = SchoolnewssubnewsTbl.query.all()
        # schoolnewssliding
        schoolnewssliding_query = SchoolnewsslidingTbl.query.all()

        return render_template('gdut_index.html', banner_site=banner_site, menu_query=menu_query,
                               topnews_href=topnews_href, topnews_title=topnews_title,
                               schoolnews_parent_href=schoolnews_parent_href,
                               schoolnews_parent_title=schoolnews_parent_title,
                               schoolnews_head_news_image=schoolnews_head_news_image,
                               schoolnews_head_news_href=schoolnews_head_news_href,
                               schoolnews_head_news_title=schoolnews_head_news_title,
                               schoolnewssubnews_query=schoolnewssubnews_query,
                               schoolnewssliding_query=schoolnewssliding_query
                               )
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
    session.execute('delete from schoolnews_tbl where 1=1')
    session.execute('delete from schoolnewssubnews_tbl where 1=1')
    session.execute('delete from schoolnewssliding_tbl where 1=1')
    session.commit()
    return render_template('clear_data.html')
