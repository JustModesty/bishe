from app import db
from app.models import *
from config import PublicGdutWebVar


# 抓取banner
def banner(html):
    banner = html.xpath('//div[@class="banner"]/img/@src')[0]
    # 存取数据库
    banner_url = banner
    banner = BannerTbl(banner_image=banner_url)
    db.session.add(banner)
    db.session.commit()


# 抓取menu
def menu(html):
    menu_link_list = html.xpath('//div[@class="menu"]/ul/li/a/@href')
    menu_name_list = html.xpath('//div[@class="menu"]/ul/li/a/text()')
    # 存入数据库
    for i in range(len(menu_link_list)):
        link = menu_link_list[i]
        name = menu_name_list[i]
        if link.startswith('http'):
            pass
        else:
            link = link
        menu = MenuTbl(menu_href=link, menu_name=name)
        db.session.add(menu)
        db.session.commit()
    # 抓取topnews
    topnews_title = html.xpath('//div[@class="topnewsc"]//h1/a/text()')[0]
    topnews_link = html.xpath('//div[@class="topnewsc"]//h1/a/@href')[0]
    # 存入数据库
    topnews = TopnewsTbl(topnews_title=topnews_title, topnews_href=topnews_link)
    db.session.add(topnews)
    db.session.commit()


# 抓取学校新闻
def schoolnews(html):
    schoolnews_parent_href = html.xpath('//div[@class="tabcenh"]/span/a/@href')[0]
    schoolnews_parent_title = html.xpath('//div[@class="tabcenh"]/span/a/text()')[0]

    schoolnews_head_news_image = html.xpath('//div[@class="ywtop2"]/div/a/img/@src')[0]
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
def schoolnewssliding(html):
    # 包含5个元素的列表
    schoolnews_head_news_image = html.xpath('//div[@class="main1right"]//div[@class="pages"]/ul/li/a/img/@src')
    # 包含5个元素的列表
    schoolnews_head_news_href = html.xpath('//div[@class="main1right"]//div[@class="pages"]/ul/li/a/@href')
    # 包含5个元素的列表
    schoolnews_head_news_title = html.xpath('//div[@class="main1right"]//div[@class="pages"]/ul/li/a/@title')

    for i in range(len(schoolnews_head_news_title)):
        link = schoolnews_head_news_href[i]
        title = schoolnews_head_news_title[i]
        image = schoolnews_head_news_image[i]
        row = SchoolnewsslidingTbl(schoolnews_head_news_image=image,
                                   schoolnews_head_news_href=link,
                                   schoolnews_head_news_title=title)
        db.session.add(row)
        db.session.commit()


# 抓取纸媒汇
def zhimeihui(html):
    title_list = html.xpath(
        '//div[@class="main3"]//div[@class="main3leftc"]/div[@class="main3leftclt"]//ul[@class="textlistuld"]/li/div/a/text()')

    link_list = html.xpath('//div[@class="main3"]//div[@class="main3leftclt"]//ul[@class="textlistuld"]/li/div/a/@href')

    for i in range(len(title_list)):
        title = title_list[i]
        link = link_list[i]
        sql_insert = Zhimeihui(paper_sub_news_href=link, paper_sub_news_title=title)
        db.session.add(sql_insert)
        db.session.commit()


# 抓取更多"更多按钮"
def more_button(html):
    more_button_list = html.xpath('//div[@class="main3"]//span[@class="gdimg"]/a/@href')
    paper_show_more_href = more_button_list[0]
    media_show_more_href = more_button_list[1]
    professor_show_more_href = more_button_list[2]
    student_show_more_href = more_button_list[3]
    higher_edu_perspective_show_more_href = more_button_list[4]
    window_politics_show_more_href = more_button_list[5]
    digitalmagazine_show_more_href = more_button_list[6]
    special_column_report_show_more_href = more_button_list[7]
    graduate_people_show_more_href = more_button_list[8]
    history_show_more_href = more_button_list[9]
    row = MoreButtonTbl(
        paper_show_more_href=paper_show_more_href,
        media_show_more_href=media_show_more_href,
        professor_show_more_href=professor_show_more_href,
        student_show_more_href=student_show_more_href,
        higher_edu_perspective_show_more_href=higher_edu_perspective_show_more_href,
        window_politics_show_more_href=window_politics_show_more_href,
        digitalmagazine_show_more_href=digitalmagazine_show_more_href,
        special_column_report_show_more_href=special_column_report_show_more_href,
        graduate_people_show_more_href=graduate_people_show_more_href,
        history_show_more_href=history_show_more_href,
    )
    db.session.add(row)
    db.session.commit()


def humanity_campus(html):
    title_list = html.xpath(
        "//div[@class='main']/div[@class='mainc']/div[@class='main3']/div[@class='main3left']/div[@class='main3leftc'][2]//li/a/text()")
    link_list = html.xpath(
        "//div[@class='main']/div[@class='mainc']/div[@class='main3']/div[@class='main3left']/div[@class='main3leftc'][2]//li/a/@href")

    for i in range(len(title_list)):
        title = title_list[i]
        link = link_list[i]
        sql_insert = HumanityCampusNew(link=link, title=title)
        db.session.add(sql_insert)
        db.session.commit()


def study_section(html):
    title_list = html.xpath(
        "//div[@class='main']/div[@class='mainc']/div[@class='main3']/div[@class='main3left']/div[@class='main3leftc'][3]//ul/li/a/text()")
    link_list = html.xpath(
        "//div[@class='main']/div[@class='mainc']/div[@class='main3']/div[@class='main3left']/div[@class='main3leftc'][3]//ul/li/a/@href")

    for i in range(len(title_list)):
        title = title_list[i]
        link = link_list[i]
        sql_insert = StudyplacesNewsTbl(link=link, title=title)
        db.session.add(sql_insert)
        db.session.commit()


def graduate_people(html):
    title_list = html.xpath(
        "//div[@class='main']/div[@class='mainc']/div[@class='main3']/div[@class='main3right']/div[@class='main3rightc'][3]/div[@class='main3rightcon']/ul[@class='textlistul']/li/div/a/text()")
    link_list = html.xpath(
        "//div[@class='main']/div[@class='mainc']/div[@class='main3']/div[@class='main3right']/div[@class='main3rightc'][3]/div[@class='main3rightcon']/ul[@class='textlistul']/li/div/a/@href")

    for i in range(len(title_list)):
        title = title_list[i]
        link = link_list[i]
        sql_insert = GraduatepeopleTbl(link=link, title=title)
        db.session.add(sql_insert)
        db.session.commit()


def shcool_history(html):
    title_list = html.xpath(
        "//div[@class='main']/div[@class='mainc']/div[@class='main3']/div[@class='main3right']/div[@class='main3rightc'][4]/div[@class='main3rightcon']/ul[@class='textlistul']/li/div/a/text()")
    link_list = html.xpath(
        "//div[@class='main']/div[@class='mainc']/div[@class='main3']/div[@class='main3right']/div[@class='main3rightc'][4]/div[@class='main3rightcon']/ul[@class='textlistul']/li/div/a/@href")

    for i in range(len(title_list)):
        title = title_list[i]
        link = link_list[i]
        sql_insert = HistoryTbl(link=link, title=title)
        db.session.add(sql_insert)
        db.session.commit()
