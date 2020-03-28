from flask import render_template
from lxml import etree

from app import db
from . import main_handler
import requests
from app.models import *
from config import PublicGdutWebVar

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

from app.main.spider_function import gdut_spider_function

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
    gdut_spider_function.banner(html)

    # 抓取Menu
    gdut_spider_function.menu(html)

    # 抓取shcoolnews
    gdut_spider_function.schoolnews(html)

    # 抓取schoolnewssliding
    gdut_spider_function.schoolnewssliding(html)

    # 抓取更多"更多按钮"
    gdut_spider_function.more_button(html)

    # 抓取纸媒汇
    gdut_spider_function.zhimeihui(html)

    # 抓取人文校园
    gdut_spider_function.humanity_campus(html)

    # 抓取学习校园
    gdut_spider_function.study_section(html)

    # 抓取校友动态
    gdut_spider_function.graduate_people(html)

    # 抓取网上校史馆
    gdut_spider_function.shcool_history(html)

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

        # more_button
        more_button_query = MoreButtonTbl.query.first()

        # 媒体工大
        # 纸媒汇
        zhimeihui_query = Zhimeihui.query.all()

        # 人文校园
        humanity_campus_query = HumanityCampusNew.query.all()

        # 学习校园
        studyplaces_news_query = StudyplacesNewsTbl.query.all()

        # 校友动态
        graduate_people_query = GraduatepeopleTbl.query.all()

        # 网上校史馆
        school_history_query = HistoryTbl.query.all()

        return render_template('show_heading_index_template.html', banner_site=banner_site, menu_query=menu_query,
                               topnews_href=topnews_href, topnews_title=topnews_title,
                               schoolnews_parent_href=schoolnews_parent_href,
                               schoolnews_parent_title=schoolnews_parent_title,
                               schoolnews_head_news_image=schoolnews_head_news_image,
                               schoolnews_head_news_href=schoolnews_head_news_href,
                               schoolnews_head_news_title=schoolnews_head_news_title,
                               schoolnewssubnews_query=schoolnewssubnews_query,
                               schoolnewssliding_query=schoolnewssliding_query,
                               more_button_query=more_button_query,
                               zhimeihui_query=zhimeihui_query,
                               humanity_campus_query=humanity_campus_query,
                               studyplaces_news_query=studyplaces_news_query,
                               graduate_people_query=graduate_people_query,
                               school_history_query=school_history_query
                               )
    else:
        return render_template('show_heading_index_template.html')


# @main_handler.route('/show_heading_index')
# def gdut_index():
#     return render_template('show_heading_index_template.html')


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
    session.execute('delete from more_button_tbl where 1=1')
    session.execute('delete from zhimeihui where 1=1')
    session.execute('delete from humanity_campus_news where 1=1')
    session.execute('delete from studyplaces_news_tbl where 1=1')
    session.execute('delete from graduatepeople_tbl where 1=1')
    session.execute('delete from history_tbl where 1=1')

    session.commit()
    return render_template('clear_data.html')


# 爬取文章详情页
@main_handler.route('/detail/<path>', methods=['GET', 'POST'])
def spider_detail(path):
    print("1111111111")
    print(type(path))
    print(path)
    print("22222222")
    return render_template('index.html')
    # return 'yourPath %s' % path
    # return render_template('show_heading_index_template.html')

