import base64
import json
import time
import uuid

import flask
from flask import render_template, redirect, url_for, request
from lxml import etree

from app import db
from . import main_handler
import requests
from app.models import *
from config import PublicGdutWebVar

from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

from app.main.spider_function import gdut_spider_function

engine = create_engine("mysql+pymysql://root:a1234567890!@127.0.0.1:3306/gdutnews", max_overflow=0, pool_size=20)
Session = sessionmaker(bind=engine)


# dashboard首页
@main_handler.route('/')
def dashboard_index():
    return render_template('index.html')


# dashboard查看数据库分类
@main_handler.route('/forum_main.html')
def dashboard_forum_main():
    return render_template('forum_main.html')


# ==================学校新闻====================================== #
# dashboard查看"学校新闻表"的数据
@main_handler.route('/table_schoolnews.html')
def dashboard_table_schoolnews():
    session = Session()
    gdutschoolnew_all_line = session.query(GdutSchoolnew.link, GdutSchoolnew.title, GdutSchoolnew.src,
                                           GdutSchoolnew.date).all()
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return render_template('table_schoolnews.html', gdutschoolnew_all_line=gdutschoolnew_all_line)


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
    # enter_url = html.xpath("//div[@class='menu']/ul/li[2]/a/@href")[0]
    gdut_spider_function.dashboard_start_spider_schoolnews_list(enter_url)

    # 爬取取完,直接重新刷新页面(每次进入那个页面的时候都会抓取数据库数据的)
    return redirect(url_for('.dashboard_table_schoolnews'))


# 学校新闻“清空数据” 接口
@main_handler.route('/clear_data_schoolnews')
def clear_data_schoolnews():
    session = Session()
    session.execute('delete from gdut_schoolnews where 1=1')
    try:
        session.commit()
    except:
        session.rollback()
    return redirect(url_for('.dashboard_table_schoolnews'))


# 学校新闻“查询” 接口
@main_handler.route('/search_data_schoolnews')
def search_data_schoolnews():
    # print(flask.request.args)
    filter_title = flask.request.args.get('product_name')
    schoolnews_query = GdutSchoolnew.query.all()
    if filter_title:
        schoolnews_query = GdutSchoolnew.query.filter(
            GdutSchoolnew.title.like("%" + filter_title + "%")
        ).all()
    return render_template('table_schoolnews.html', gdutschoolnew_all_line=schoolnews_query)


# 学校新闻“编辑” 接口
@main_handler.route('/schoolnews_edit')
def edit_article_schoolnews():
    # 1. 定位是哪篇文章
    article_title_restful_url = flask.request.args.get('article_link')
    print("article_title=", article_title_restful_url)

    # 2. 查询数据库,找到文章内容
    session = Session()
    article_id_in_mysql = session.execute(
        "select id from gdut_detailpage where link='%s';" % (article_title_restful_url))
    article_id_in_mysql_first = article_id_in_mysql.first()
    article_id_in_mysql_first_zero = article_id_in_mysql_first[0]
    try:
        session.commit()
    except:
        session.rollback()
    content = gdut_spider_function.query_from_database_gdut_detailpage(article_title_restful_url)

    # 3. 返回内容并渲染成一个新页面
    return render_template('ecommerce_product.html', content=content, article_link=article_title_restful_url,
                           article_id_in_mysql=article_id_in_mysql_first_zero, news_class="schoolnews")


# 学校新闻编辑里面的"保存修改"按钮
@main_handler.route('/save_schoolnews_edit', methods=['GET', 'POST'])
def save_edit_article_schoolnews():
    # 1. 定位是哪篇文章
    if request.method == 'POST':
        databases_map = {'schoolnews': GdutSchoolnew, }
        databases_map_content = {'schoolnews': GdutDetailpageContent}
        databases_map_picture = {'schoolnews': GdutDetailpagePicture}
        update_field = flask.request.args.get('update_field')
        news_class = flask.request.args.get('news_class')
        article_id = request.form['mysql_id']
        article = GdutDetailpage.query.get(article_id)


        if update_field == 'title':
            link = article.link
            row = databases_map[news_class].query.filter(databases_map[news_class].link == link).first()

            new_title = request.form['title']
            article.title = new_title
            row.title =  new_title
            try:
                db.session.commit()
            except:
                db.session.rollback()
        if update_field == 'date':
            link = article.link
            row = databases_map[news_class].query.filter(databases_map[news_class].link == link).first()

            new_date = request.form['date']
            article.date = new_date
            row.date = new_date
            try:
                db.session.commit()
            except:
                db.session.rollback()
        if update_field == 'jianjie':
            new_jianjie = request.form['jianjie']
            article.jianjie = new_jianjie
            try:
                db.session.commit()
            except:
                db.session.rollback()
        if update_field == 'paragraph':
            link = article.link
            new_paragraph = request.form['paragraph']
            # print("paragraph=", new_paragraph)
            html = etree.HTML(new_paragraph)
            picture_html_list = html.xpath('//img/@src')
            # fixme:新插入的图片是base64编码,需要下载到本地,然后数据库存储本地地址
            picture_rows = databases_map_picture[news_class].query.filter(databases_map_picture[news_class].detail_link == link).all()
            for row in picture_rows:
                try:
                    db.session.delete(row)
                    db.session.commit()
                except :
                    db.session.rollback()
            for picture in picture_html_list:
                print("picture=", picture)
                if picture.startswith("data"):
                    start_index = picture.find(',') + 1
                    base64_str = picture[start_index:]
                    # 只能放jpg格式的图片!
                    random_str = str(uuid.uuid4()) + ".jpg"
                    file_name = "app/static/gdut_img/detailpage/" + random_str
                    with open(file_name, 'wb') as f:
                        f.write(base64.b64decode(base64_str))
                    save_position = 'app/static/gdut_img/detailpage/' + random_str
                    sql_insert_GdutDetailpagePicture = GdutDetailpagePicture(detail_link=link, local_position=save_position)
                    db.session.add(sql_insert_GdutDetailpagePicture)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()
                else:
                    save_position = "app" + picture[2:]
                    sql_insert_GdutDetailpagePicture = GdutDetailpagePicture(detail_link=link,
                                                                             local_position=save_position)
                    db.session.add(sql_insert_GdutDetailpagePicture)

                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()




            text_list = html.xpath('//p/text()')
            content_rows = databases_map_content[news_class].query.filter(databases_map_content[news_class].detail_link == link).all()
            for row in content_rows:
                try:
                    db.session.delete(row)
                    db.session.commit()
                except :
                    db.session.rollback()
            for text in text_list:
                try:
                    row = databases_map_content[news_class](detail_link=link, paragraph=text)
                    db.session.add(row)
                    db.session.commit()
                except :
                    db.session.rollback()



            #
            # article.jianjie = new_jianjie
            # try:
            #     db.session.commit()
            # except:
            #     db.session.rollback()

        # content = eval(content)

        # 2. 查询数据库,找到文章内容
        # content['title'] = str(title)
        # content['date'] = str(date)
        # content['jianjie'] = str(jianjie)

        # # 3. 返回内容并渲染成一个新页面
        # todo:以后更改为跳转到用户的展示页面
        return redirect(url_for('.dashboard_table_schoolnews'))


# # 1. 定位是哪篇文章
# if request.method == 'POST':
#     origin_title = request.form['origin_title']
#     title = request.form['title']
#     date = request.form['date']
#     jianjie = request.form['jianjie']
#     origin_title = flask.request.args.get('origin_title')
#     content = flask.request.args.get('ret_content')
#
#     content = eval(content)
#
#     # 2. 查询数据库,找到文章内容
#     content['title'] = str(title)
#     content['date'] = str(date)
#     content['jianjie'] = str(jianjie)
#
#     # # 3. 返回内容并渲染成一个新页面
#     # todo:以后更改为跳转到用户的展示页面
#     return redirect(url_for('.dashboard_table_schoolnews'))


# ==================工大====================================== #
# dashboard查看"媒体工大表"的数据
@main_handler.route('/table_meitigongda.html')
def dashboard_table_meitigongda():
    session = Session()
    gdutschoolnew_all_line = session.query(GdutMeitigongda.link, GdutMeitigongda.title, GdutMeitigongda.src,
                                           GdutMeitigongda.date).all()
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return render_template('table_meitigongda.html', gdutschoolnew_all_line=gdutschoolnew_all_line)


# dashboard 媒体工大 “开始爬取” 接口
@main_handler.route('/dashboard_start_spider_meitigongda')
def dashboard_start_spider_meitigongda():
    response = requests.get('http://gdutnews.gdut.edu.cn/')
    content = response.content
    content = content.decode('utf-8')
    html = etree.HTML(content)

    # 抓取shcoolnews
    # gdut_spider_function.meitigongda(html)

    # 从菜单栏里面找到入口
    enter_url = html.xpath("//div[@class='menu']/ul/li[4]/a/@href")[0]
    gdut_spider_function.dashboard_start_spider_meitigongda_list(enter_url)

    # 爬取取完,直接重新刷新页面(每次进入那个页面的时候都会抓取数据库数据的)
    return redirect(url_for('.dashboard_table_meitigongda'))


# 媒体工大“清空数据” 接口
@main_handler.route('/clear_data_meitigongda')
def clear_data_meitigongda():
    session = Session()
    session.execute('delete from gdut_meitigongda where 1=1')
    try:
        session.commit()
    except:
        session.rollback()
    return redirect(url_for('.dashboard_table_meitigongda'))


# 媒体工大“查询” 接口
@main_handler.route('/search_data_meitigongda')
def search_data_meitigongda():
    # print(flask.request.args)
    filter_title = flask.request.args.get('product_name')
    meitigongda_query = GdutMeitigongda.query.all()
    if filter_title:
        meitigongda_query = GdutMeitigongda.query.filter(
            GdutMeitigongda.title.like("%" + filter_title + "%")
        ).all()
    return render_template('table_meitigongda.html', gdutschoolnew_all_line=meitigongda_query)


# 媒体工大“编辑” 接口
@main_handler.route('/meitigongda_edit')
def edit_article_meitigongda():
    # 1. 定位是哪篇文章
    article_title_restful_url = flask.request.args.get('article_link')
    # print("article_title=", article_title_restful_url)

    # 2. 查询数据库,找到文章内容
    content = gdut_spider_function.query_from_database_gdut_detailpage(article_title_restful_url)

    # 3. 返回内容并渲染成一个新页面
    return render_template('ecommerce_product.html', content=content, article_link=article_title_restful_url)


# 媒体工大编辑里面的"保存修改"按钮
@main_handler.route('/save_meitigongda_edit', methods=['GET', 'POST'])
def save_edit_article_meitigongda():
    # 1. 定位是哪篇文章
    if request.method == 'POST':
        update_field = flask.request.args.get('update_field')
        article_id = request.form['mysql_id']
        if update_field == 'title':
            new_title = request.form['title']
            session = Session()
            cursor = session.execute(
                "update gdut_detailpage set title='%s' where id='%d';" % (new_title, int(article_id)))
            try:
                session.commit()
            except:
                session.rollback()
        if update_field == 'date':
            pass
        if update_field == 'jianjie':
            pass
        if update_field == 'paragraph':
            pass

        # content = eval(content)

        # 2. 查询数据库,找到文章内容
        # content['title'] = str(title)
        # content['date'] = str(date)
        # content['jianjie'] = str(jianjie)

        # # 3. 返回内容并渲染成一个新页面
        # todo:以后更改为跳转到用户的展示页面
        return redirect(url_for('.dashboard_table_meitigongda'))


# ==================人文校园====================================== #
# dashboard查看"人文校园表"的数据
@main_handler.route('/table_renwenxiaoyuan.html')
def dashboard_table_renwenxiaoyuan():
    session = Session()
    gdutschoolnew_all_line = session.query(GdutRenwenxiaoyuan.link, GdutRenwenxiaoyuan.title, GdutRenwenxiaoyuan.src,
                                           GdutRenwenxiaoyuan.date).all()
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return render_template('table_renwenxiaoyuan.html', gdutschoolnew_all_line=gdutschoolnew_all_line)


# dashboard 人文校园 “开始爬取” 接口
@main_handler.route('/dashboard_start_spider_renwenxiaoyuan')
def dashboard_start_spider_renwenxiaoyuan():
    response = requests.get('http://gdutnews.gdut.edu.cn/')
    content = response.content
    content = content.decode('utf-8')
    html = etree.HTML(content)

    # 从菜单栏里面找到入口
    enter_url = html.xpath("//div[@class='menu']/ul/li[6]/a/@href")[0]
    gdut_spider_function.dashboard_start_spider_renwenxiaoyuan_list(enter_url)

    # 爬取取完,直接重新刷新页面(每次进入那个页面的时候都会抓取数据库数据的)
    return redirect(url_for('.dashboard_table_renwenxiaoyuan'))


# 人文校园“清空数据” 接口
@main_handler.route('/clear_data_renwenxiaoyuan')
def clear_data_renwenxiaoyuan():
    session = Session()
    session.execute('delete from gdut_renwenxiaoyuan where 1=1')
    try:
        session.commit()
    except:
        session.rollback()
    return redirect(url_for('.dashboard_table_renwenxiaoyuan'))


# 人文校园“查询” 接口
@main_handler.route('/search_data_renwenxiaoyuan')
def search_data_renwenxiaoyuan():
    # print(flask.request.args)
    filter_title = flask.request.args.get('product_name')
    meitigongda_query = GdutRenwenxiaoyuan.query.all()
    if filter_title:
        meitigongda_query = GdutRenwenxiaoyuan.query.filter(
            GdutRenwenxiaoyuan.title.like("%" + filter_title + "%")
        ).all()
    return render_template('table_renwenxiaoyuan.html', gdutschoolnew_all_line=meitigongda_query)


# 人文校园“编辑” 接口
@main_handler.route('/renwenxiaoyuan_edit')
def edit_article_renwenxiaoyuan():
    # 1. 定位是哪篇文章
    article_title_restful_url = flask.request.args.get('article_link')
    # print("article_title=", article_title_restful_url)

    # 2. 查询数据库,找到文章内容
    content = gdut_spider_function.query_from_database_gdut_detailpage(article_title_restful_url)

    # 3. 返回内容并渲染成一个新页面
    return render_template('ecommerce_product.html', content=content, article_link=article_title_restful_url)


# 人文校园编辑里面的"保存修改"按钮
@main_handler.route('/save_renwenxiaoyuan_edit', methods=['GET', 'POST'])
def save_edit_article_renwenxiaoyuan():
    # 1. 定位是哪篇文章
    if request.method == 'POST':
        origin_title = request.form['origin_title']
        title = request.form['title']
        date = request.form['date']
        jianjie = request.form['jianjie']
        origin_title = flask.request.args.get('origin_title')
        content = flask.request.args.get('ret_content')

        content = eval(content)

        # 2. 查询数据库,找到文章内容
        content['title'] = str(title)
        content['date'] = str(date)
        content['jianjie'] = str(jianjie)

        # # 3. 返回内容并渲染成一个新页面
        # todo:以后更改为跳转到用户的展示页面
        return redirect(url_for('.dashboard_table_renwenxiaoyuan'))


# ==================校友动态表====================================== #
# dashboard查看"校友动态"的数据
@main_handler.route('/table_xiaoyoudongtai.html')
def dashboard_table_xiaoyoudongtai():
    session = Session()
    gdutschoolnew_all_line = session.query(GdutXiaoyoudongtai.link, GdutXiaoyoudongtai.title, GdutXiaoyoudongtai.src,
                                           GdutXiaoyoudongtai.date).all()
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return render_template('table_xiaoyoudongtai.html', gdutschoolnew_all_line=gdutschoolnew_all_line)


# dashboard 校友动态 “开始爬取” 接口
@main_handler.route('/dashboard_start_spider_xiaoyoudongtai')
def dashboard_start_spider_xiaoyoudongtai():
    response = requests.get('http://gdutnews.gdut.edu.cn/')
    content = response.content
    content = content.decode('utf-8')
    html = etree.HTML(content)

    # 从菜单栏里面找到入口
    enter_url = html.xpath("//div[@class='menu']/ul/li[7]/a/@href")[0]
    gdut_spider_function.dashboard_start_spider_xiaoyoudongtai_list(enter_url)

    # 爬取取完,直接重新刷新页面(每次进入那个页面的时候都会抓取数据库数据的)
    return redirect(url_for('.dashboard_table_xiaoyoudongtai'))


# 校友动态“清空数据” 接口
@main_handler.route('/clear_data_xiaoyoudongtai')
def clear_data_xiaoyoudongtai():
    session = Session()
    session.execute('delete from gdut_xiaoyoudongtai where 1=1')
    try:
        session.commit()
    except:
        session.rollback()
    return redirect(url_for('.dashboard_table_xiaoyoudongtai'))


# 校友动态“查询” 接口
@main_handler.route('/search_data_xiaoyoudongtai')
def search_data_xiaoyoudongtai():
    # print(flask.request.args)
    filter_title = flask.request.args.get('product_name')
    meitigongda_query = GdutXiaoyoudongtai.query.all()
    if filter_title:
        meitigongda_query = GdutXiaoyoudongtai.query.filter(
            GdutXiaoyoudongtai.title.like("%" + filter_title + "%")
        ).all()
    return render_template('table_xiaoyoudongtai.html', gdutschoolnew_all_line=meitigongda_query)


# 校友动态“编辑” 接口
@main_handler.route('/xiaoyoudongtai_edit')
def edit_article_xiaoyoudongtai():
    # 1. 定位是哪篇文章
    article_title_restful_url = flask.request.args.get('article_link')
    # print("article_title=", article_title_restful_url)

    # 2. 查询数据库,找到文章内容
    content = gdut_spider_function.query_from_database_gdut_detailpage(article_title_restful_url)

    # 3. 返回内容并渲染成一个新页面
    return render_template('ecommerce_product.html', content=content, article_link=article_title_restful_url)


# 校友动态编辑里面的"保存修改"按钮
@main_handler.route('/save_xiaoyoudongtai_edit', methods=['GET', 'POST'])
def save_edit_article_xiaoyoudongtai():
    # 1. 定位是哪篇文章
    if request.method == 'POST':
        origin_title = request.form['origin_title']
        title = request.form['title']
        date = request.form['date']
        jianjie = request.form['jianjie']
        origin_title = flask.request.args.get('origin_title')
        content = flask.request.args.get('ret_content')

        content = eval(content)

        # 2. 查询数据库,找到文章内容
        content['title'] = str(title)
        content['date'] = str(date)
        content['jianjie'] = str(jianjie)

        # # 3. 返回内容并渲染成一个新页面
        # todo:以后更改为跳转到用户的展示页面
        return redirect(url_for('.dashboard_table_xiaoyoudongtai'))


# ==================网上校史馆====================================== #
# dashboard查看"校友动态"的数据
@main_handler.route('/table_wangshangxiaoshiguan.html')
def dashboard_table_wangshangxiaoshiguan():
    session = Session()
    gdutschoolnew_all_line = session.query(GdutWangshangxiaoshiguan.link, GdutWangshangxiaoshiguan.title,
                                           GdutWangshangxiaoshiguan.src,
                                           GdutWangshangxiaoshiguan.date).all()
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return render_template('table_wangshangxiaoshiguan.html', gdutschoolnew_all_line=gdutschoolnew_all_line)


# dashboard 校友动态 “开始爬取” 接口
@main_handler.route('/dashboard_start_spider_wangshangxiaoshiguan')
def dashboard_start_spider_wangshangxiaoshiguan():
    response = requests.get('http://gdutnews.gdut.edu.cn/')
    content = response.content
    content = content.decode('utf-8')
    html = etree.HTML(content)

    # 从菜单栏里面找到入口
    enter_url = html.xpath("//div[@class='menu']/ul/li[7]/a/@href")[0]
    gdut_spider_function.dashboard_start_spider_wangshangxiaoshiguan_list(enter_url)

    # 爬取取完,直接重新刷新页面(每次进入那个页面的时候都会抓取数据库数据的)
    return redirect(url_for('.dashboard_table_wangshangxiaoshiguan'))


# 校友动态“清空数据” 接口
@main_handler.route('/clear_data_wangshangxiaoshiguan')
def clear_data_wangshangxiaoshiguan():
    session = Session()
    session.execute('delete from gdut_wangshangxiaoshiguan where 1=1')
    try:
        session.commit()
    except:
        session.rollback()
    return redirect(url_for('.dashboard_table_wangshangxiaoshiguan'))


# 校友动态“查询” 接口
@main_handler.route('/search_data_wangshangxiaoshiguan')
def search_data_wangshangxiaoshiguan():
    # print(flask.request.args)
    filter_title = flask.request.args.get('product_name')
    meitigongda_query = GdutWangshangxiaoshiguan.query.all()
    if filter_title:
        meitigongda_query = GdutWangshangxiaoshiguan.query.filter(
            GdutWangshangxiaoshiguan.title.like("%" + filter_title + "%")
        ).all()
    return render_template('table_wangshangxiaoshiguan.html', gdutschoolnew_all_line=meitigongda_query)


# 校友动态“编辑” 接口
@main_handler.route('/wangshangxiaoshiguan_edit')
def edit_article_wangshangxiaoshiguan():
    # 1. 定位是哪篇文章
    article_title_restful_url = flask.request.args.get('article_link')
    # print("article_title=", article_title_restful_url)

    # 2. 查询数据库,找到文章内容
    content = gdut_spider_function.query_from_database_gdut_detailpage(article_title_restful_url)

    # 3. 返回内容并渲染成一个新页面
    return render_template('ecommerce_product.html', content=content, article_link=article_title_restful_url)


# 校友动态编辑里面的"保存修改"按钮
@main_handler.route('/save_wangshangxiaoshiguan_edit', methods=['GET', 'POST'])
def save_edit_article_wangshangxiaoshiguan():
    # 1. 定位是哪篇文章
    if request.method == 'POST':
        origin_title = request.form['origin_title']
        title = request.form['title']
        date = request.form['date']
        jianjie = request.form['jianjie']
        origin_title = flask.request.args.get('origin_title')
        content = flask.request.args.get('ret_content')

        content = eval(content)

        # 2. 查询数据库,找到文章内容
        content['title'] = str(title)
        content['date'] = str(date)
        content['jianjie'] = str(jianjie)

        # # 3. 返回内容并渲染成一个新页面
        # todo:以后更改为跳转到用户的展示页面
        return redirect(url_for('.dashboard_table_wangshangxiaoshiguan'))


# ==================学习园地表====================================== #
# dashboard查看"学习园地表"的数据
# @main_handler.route('/table_xuexiyuandi.html')
# def dashboard_table_xuexiyuandi():
#     return render_template('table_xuexiyuandi.html')

# dashboard查看"校友动态"的数据
@main_handler.route('/table_xuexiyuandi.html')
def dashboard_table_xuexiyuandi():
    session = Session()
    gdutschoolnew_all_line = session.query(GdutXuexiyuandi.link, GdutXuexiyuandi.title, GdutXuexiyuandi.src,
                                           GdutXuexiyuandi.date).all()
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return render_template('table_xuexiyuandi.html', gdutschoolnew_all_line=gdutschoolnew_all_line)


# dashboard 校友动态 “开始爬取” 接口
@main_handler.route('/dashboard_start_spider_xuexiyuandi')
def dashboard_start_spider_xuexiyuandi():
    response = requests.get('http://gdutnews.gdut.edu.cn/')
    content = response.content
    content = content.decode('utf-8')
    html = etree.HTML(content)

    # 从菜单栏里面找到入口
    enter_url = html.xpath("//div[@class='menu']/ul/li[8]/a/@href")[0]
    gdut_spider_function.dashboard_start_spider_xuexiyuandi_list(enter_url)

    # 爬取取完,直接重新刷新页面(每次进入那个页面的时候都会抓取数据库数据的)
    return redirect(url_for('.dashboard_table_xuexiyuandi'))


# 校友动态“清空数据” 接口
@main_handler.route('/clear_data_xuexiyuandi')
def clear_data_xuexiyuandi():
    session = Session()
    session.execute('delete from gdut_xuexiyuandi where 1=1')
    try:
        session.commit()
    except:
        session.rollback()
    return redirect(url_for('.dashboard_table_xuexiyuandi'))


# 校友动态“查询” 接口
@main_handler.route('/search_data_xuexiyuandi')
def search_data_xuexiyuandi():
    # print(flask.request.args)
    filter_title = flask.request.args.get('product_name')
    meitigongda_query = GdutXuexiyuandi.query.all()
    if filter_title:
        meitigongda_query = GdutXuexiyuandi.query.filter(
            GdutXuexiyuandi.title.like("%" + filter_title + "%")
        ).all()
    return render_template('table_xuexiyuandi.html', gdutschoolnew_all_line=meitigongda_query)


# 校友动态“编辑” 接口
@main_handler.route('/xuexiyuandi_edit')
def edit_article_xuexiyuandi():
    # 1. 定位是哪篇文章
    article_title_restful_url = flask.request.args.get('article_link')
    # print("article_title=", article_title_restful_url)

    # 2. 查询数据库,找到文章内容
    content = gdut_spider_function.query_from_database_gdut_detailpage(article_title_restful_url)

    # 3. 返回内容并渲染成一个新页面
    return render_template('ecommerce_product.html', content=content, article_link=article_title_restful_url)


# 校友动态编辑里面的"保存修改"按钮
@main_handler.route('/save_xuexiyuandi_edit', methods=['GET', 'POST'])
def save_edit_article_xuexiyuandi():
    # 1. 定位是哪篇文章
    if request.method == 'POST':
        origin_title = request.form['origin_title']
        title = request.form['title']
        date = request.form['date']
        jianjie = request.form['jianjie']
        origin_title = flask.request.args.get('origin_title')
        content = flask.request.args.get('ret_content')

        content = eval(content)

        # 2. 查询数据库,找到文章内容
        content['title'] = str(title)
        content['date'] = str(date)
        content['jianjie'] = str(jianjie)

        # # 3. 返回内容并渲染成一个新页面
        # todo:以后更改为跳转到用户的展示页面
        return redirect(url_for('.dashboard_table_xuexiyuandi'))


# ===================专栏报道表=========================================== #

# dashboard查看"校友动态"的数据
@main_handler.route('/table_zhuanlanbaodao.html')
def dashboard_table_zhuanlanbaodao():
    session = Session()
    gdutschoolnew_all_line = session.query(GdutZhuanlanbaodao.link, GdutZhuanlanbaodao.title, GdutZhuanlanbaodao.src,
                                           GdutZhuanlanbaodao.date).all()
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return render_template('table_zhuanlanbaodao.html', gdutschoolnew_all_line=gdutschoolnew_all_line)


# dashboard 校友动态 “开始爬取” 接口
@main_handler.route('/dashboard_start_spider_zhuanlanbaodao')
def dashboard_start_spider_zhuanlanbaodao():
    response = requests.get('http://gdutnews.gdut.edu.cn/')
    content = response.content
    content = content.decode('utf-8')
    html = etree.HTML(content)

    # 从菜单栏里面找到入口
    enter_url = html.xpath("//div[@class='menu']/ul/li[9]/a/@href")[0]
    gdut_spider_function.dashboard_start_spider_zhuanlanbaodao_list(enter_url)

    # 爬取取完,直接重新刷新页面(每次进入那个页面的时候都会抓取数据库数据的)
    return redirect(url_for('.dashboard_table_zhuanlanbaodao'))


# 校友动态“清空数据” 接口
@main_handler.route('/clear_data_zhuanlanbaodao')
def clear_data_zhuanlanbaodao():
    session = Session()
    session.execute('delete from gdut_zhuanlanbaodao where 1=1')
    try:
        session.commit()
    except:
        session.rollback()
    return redirect(url_for('.dashboard_table_zhuanlanbaodao'))


# 校友动态“查询” 接口
@main_handler.route('/search_data_zhuanlanbaodao')
def search_data_zhuanlanbaodao():
    # print(flask.request.args)
    filter_title = flask.request.args.get('product_name')
    meitigongda_query = GdutZhuanlanbaodao.query.all()
    if filter_title:
        meitigongda_query = GdutZhuanlanbaodao.query.filter(
            GdutZhuanlanbaodao.title.like("%" + filter_title + "%")
        ).all()
    return render_template('table_zhuanlanbaodao.html', gdutschoolnew_all_line=meitigongda_query)


# 校友动态“编辑” 接口
@main_handler.route('/zhuanlanbaodao_edit')
def edit_article_zhuanlanbaodao():
    # 1. 定位是哪篇文章
    article_title_restful_url = flask.request.args.get('article_link')
    # print("article_title=", article_title_restful_url)

    # 2. 查询数据库,找到文章内容
    content = gdut_spider_function.query_from_database_gdut_detailpage(article_title_restful_url)

    # 3. 返回内容并渲染成一个新页面
    return render_template('ecommerce_product.html', content=content, article_link=article_title_restful_url)


# 校友动态编辑里面的"保存修改"按钮
@main_handler.route('/save_zhuanlanbaodao_edit', methods=['GET', 'POST'])
def save_edit_article_zhuanlanbaodao():
    # 1. 定位是哪篇文章
    if request.method == 'POST':
        origin_title = request.form['origin_title']
        title = request.form['title']
        date = request.form['date']
        jianjie = request.form['jianjie']
        origin_title = flask.request.args.get('origin_title')
        content = flask.request.args.get('ret_content')

        content = eval(content)

        # 2. 查询数据库,找到文章内容
        content['title'] = str(title)
        content['date'] = str(date)
        content['jianjie'] = str(jianjie)

        # # 3. 返回内容并渲染成一个新页面
        # todo:以后更改为跳转到用户的展示页面
        return redirect(url_for('.dashboard_table_zhuanlanbaodao'))


# ========================================================================

# dashboard里面点击文章之后,跳转到"编辑"页面
@main_handler.route('/ecommerce_product.html', methods=['GET'])
def dashboard_jump_edit():
    # print("article_link=", article_link)
    print(flask.request.args.get('article_link'))
    if_exist = db.session.query(GdutSchoolnewsDetailpage.link == path).first()

    # todo:查询文章内容的详情

    return render_template('ecommerce_product.html')


# 模拟的爬取到的新闻首页
@main_handler.route('/landing.html')
def gdutnews_index():
    # return render_template('landing.html')
    # banner
    session = Session()
    cursor = session.execute('select count(*) from banner_tbl')
    try:
        session.commit()
    except:
        session.rollback()
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
    try:
        session.commit()
    except:
        session.rollback()
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
    session.execute('delete from gdut_detailpage where 1=1')
    session.execute('delete from gdut_detailpage_content where 1=1')
    session.execute('delete from gdut_detailpage_picture where 1=1')

    try:
        session.commit()
    except:
        session.rollback()
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
            else:
                text_list.append(content.text)

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
