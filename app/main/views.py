import time

import flask
from flask import render_template, redirect, url_for
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


# dashboard首页
@main_handler.route('/')
def dashboard_index():
    return render_template('index.html')


# dashboard查看数据库分类
@main_handler.route('/forum_main.html')
def dashboard_forum_main():
    return render_template('forum_main.html')

# dashboard查看"学校新闻表"的数据
@main_handler.route('/table_schoolnews.html')
def dashboard_table_schoolnews():
    session = Session()
    gdutschoolnew_all_line = session.query(GdutSchoolnew.link, GdutSchoolnew.title, GdutSchoolnew.src, GdutSchoolnew.date).all()
    # session.add(gdutschoolnew_all_line)
    db.session.commit()
    return render_template('table_schoolnews.html', gdutschoolnew_all_line=gdutschoolnew_all_line)

# dashboard查看"媒体工大表"的数据
@main_handler.route('/table_meitigongda.html')
def dashboard_table_meitigongda():
    return render_template('table_meitigongda.html')

# dashboard查看"人文校园表"的数据
@main_handler.route('/table_renwenxiaoyuan.html')
def dashboard_table_renwenxiaoyuan():
    return render_template('table_renwenxiaoyuan.html')


# dashboard查看"校友动态表"的数据
@main_handler.route('/table_xiaoyoudongtai.html')
def dashboard_table_xiaoyoudongtai():
    return render_template('table_xiaoyoudongtai.html')


# dashboard查看"网上校史馆表"的数据
@main_handler.route('/table_wangshangxiaoshiguan.html')
def dashboard_table_wangshangxiaoshiguan():
    return render_template('table_wangshangxiaoshiguan.html')


# dashboard查看"学习园地表"的数据
@main_handler.route('/table_xuexiyuandi.html')
def dashboard_table_xuexiyuandi():
    return render_template('table_xuexiyuandi.html')

# dashboard里面点击文章之后,跳转到"编辑"页面
@main_handler.route('/ecommerce_product.html', methods=['GET'])
def dashboard_jump_edit():
    # print("article_link=", article_link)
    print(flask.request.args.get('article_link'))
    if_exist = db.session.query(GdutSchoolnewsDetailpage.link == path).first()

    # todo:查询文章内容的详情

    return render_template('ecommerce_product.html')

# dashboard 学校新闻 “开始爬取” 接口
@main_handler.route('/dashboard_start_spider_schoolnews')
def dashboard_start_spider_schoolnews():
    response = requests.get('http://gdutnews.gdut.edu.cn/')
    content = response.content
    content = content.decode('utf-8')
    html = etree.HTML(content)

    # 抓取shcoolnews
    # gdut_spider_function.schoolnews(html)

    # 从菜单栏里面找到入口
    enter_url = html.xpath("//div[@class='menu']/ul/li[2]/a/@href")[0]
    gdut_spider_function.dashboard_start_spider_schoolnews_list(enter_url)

    # 爬取取完,直接重新刷新页面(每次进入那个页面的时候都会抓取数据库数据的)
    return redirect(url_for('.dashboard_table_schoolnews'))

# “清空数据” 接口
@main_handler.route('/clear_data_schoolnews')
def clear_data_schoolnews():
    # 删除banner
    session = Session()
    session.execute('delete from gdut_schoolnews where 1=1')
    session.commit()
    # return redirect(url_for('.dashboard_table_schoolnews'))
    return redirect(url_for('.dashboard_table_schoolnews'))


# 模拟的爬取到的新闻首页
@main_handler.route('/landing.html')
def gdutnews_index():
    # return render_template('landing.html')
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

        return render_template('landing.html', banner_site=banner_site, menu_query=menu_query,
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
        return render_template('landing.html')

@main_handler.route('/my_gdut_index')
def index():
    return render_template('my_gdut_index.html')


# “开始爬取” 接口
@main_handler.route('/start_spider')
def start_spider123():
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
    session.execute('delete from gdut_schoolnews where 1=1')

    session.commit()
    return render_template('clear_data.html')


# 爬取文章详情页,并且渲染成为一个新页面并展示
@main_handler.route('/detail/<path>', methods=['GET'])
def spider_detail(path):
    if path.startswith('http'):
        # todo:如果是http开头: 直接新标签跳转
        pass
    # 其他情况:
    else:
        # url = PublicGdutWebVar.url_pre + path

        # 爬取文章, 标题,内容 todo:存入数据库,下次直接从数据库提取
        detail = gdut_spider_function.start_spider_detail(path)
        title = detail['title'][0]
        jianjie = detail['jianjie'][0].strip()
        content_list = detail['content_list']
        content_list2 = detail['content_list2']

        img_list = detail['img_list']
        text_list = []
        for content in content_list:
            if content.text is None:
                pass
                # text_list.append("None")
            else:
                text_list.append(content.text)
        # for content in content_list2:
        #     text_list.append(content.text)

        for content in content_list2:
            text_list.append(str(content))

        img_link_list = []
        for link in img_list:
            img_link_list.append(PublicGdutWebVar.url_pre + link)
        release_date = detail['release_date'][0]
        # 取出标题和内容,传递给前端
        return render_template('detail_page.html', title=title, jianjie=jianjie, text_list=text_list,
                               img_link_list=img_link_list, release_date=release_date)


# 爬取菜单里的专题跳转的页面,并且渲染成为一个新页面并展示
# 有几个专题的页面模板是相同的:学校新闻, 图片新闻, 媒体工大, 人文校园, 学习园地, 专题报道  这六个可以用这个接口
@main_handler.route('/menu_section/<path>', methods=['GET'])
def spider_menu_section(path):
    url = PublicGdutWebVar.url_pre + path

    # 爬取链接  todo:存入数据库,下次直接从数据库提取
    all_news = gdut_spider_function.start_spider_menu_section(url)

    return render_template('menu_section_page.html', all_news=all_news)
