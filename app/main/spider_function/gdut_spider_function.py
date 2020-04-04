import requests
from lxml import etree

from app import db
from app.models import *
from config import PublicGdutWebVar

from urllib.request import urlretrieve

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
        print("5555555555555555555555555555555555555")
        print(type(link))
        print(link)
        print("66666666666666666666666666666666666666")
        title = schoolnews_sub_news_title[i]
        print(type(title))
        print(title)
        print("777777777777777777777777777777777777777")
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


def start_spider_detail(path):
    url = PublicGdutWebVar.url_pre + path
    response = requests.get(url)
    content = response.content
    content = content.decode('utf-8')
    html = etree.HTML(content)

    detail = {}



    if_exist = db.session.query(GdutDetailpage.link == path).first()
    # 如果没有爬取过这个文章,在这里进行爬取
    if if_exist is None:
        detail['title'] = html.xpath("//div[@class='newslistcon']/div[@class='listleft']/div[@class='contentmain']/form/h1[@class='title']/span[@id='ctl00_ContentPlaceHolder1_tbxTitle']/text()")
        detail['release_date'] = html.xpath("///div[@class='newslistcon']/div[@class='listleft']/div[@class='contentmain']/form/div[@class='info']/span[@id='ctl00_ContentPlaceHolder1_tbxUpdateTime']/text()")
        detail['jianjie'] = html.xpath("//div[@class='newslistcon']/div[@class='listleft']/div[@class='contentmain']/form/div[@id='ctl00_ContentPlaceHolder1_jj']/p/span[@id='ctl00_ContentPlaceHolder1_tbxIntro']/text()")
        detail['content_list'] = html.xpath('//div[@id="vsb_content_2"]//p//span')
        detail['content_list2'] = html.xpath('//div[@id="vsb_content_4"]//p//text()')
        detail['img_list'] = html.xpath('//div[@id="vsb_content_2"]//p//img/@src')


        # 存储文章基本信息
        sql_insert_GdutSchoolnewsDetailpage = GdutDetailpage(link=path, title=detail['title'], date=detail['release_date'], jianjie=detail['jianjie'])
        db.session.add(sql_insert_GdutSchoolnewsDetailpage)

        # 下载图片
        for img_item in detail['img_list']:
            start_index = img_item.rfind('/')
            save_position = 'app/static/gdut_img/detailpage' + img_item[start_index:]
            urlretrieve(PublicGdutWebVar.url_pre_no_slash + img_item, save_position)
            sql_insert_GdutDetailpagePicture = GdutDetailpagePicture(detail_link=path, local_position=save_position)
            db.session.add(sql_insert_GdutDetailpagePicture)

        # 存储段落
        text_list = []
        for content in detail['content_list']:
            if content.text is None:
                pass
                # text_list.append("None")
            else:
                text_list.append(content.text)
        # for content in content_list2:
        #     text_list.append(content.text)

        for content in detail['content_list2']:
            text_list.append(str(content))

        # for paragraph in detail['content_list']:
        #     pass
        # for paragraph in detail['content_list2']:
        #     pass
        for paragraph in text_list:
            sql_insert_GdutDetailpageContent = GdutDetailpageContent(detail_link=path, paragraph=paragraph)
            db.session.add(sql_insert_GdutDetailpageContent)
        db.session.commit()
    return detail


def start_spider_menu_section(url):
    response = requests.get(url)
    content = response.content
    content = content.decode('utf-8')
    html = etree.HTML(content)

    all_news = []

    # 有图片的位于顶部的新闻
    # 图片的src链接(不含前缀)
    top_news_src_links = html.xpath("//ul[@class='listimgul']//li//img/@src")
    # 新闻的链接(部分含含http前缀的外部链接,直接跳转；不含的则加广工前缀跳转)
    top_news_links = html.xpath("//ul[@class='listimgul']//li//a[@class='listimgulimg']/@href")
    # 顶部新闻标题
    top_news_titles = html.xpath("//a[@class='listimgultitle']/text()")
    for i in range(len(top_news_src_links)):
        item = {'src': PublicGdutWebVar.url_pre + top_news_src_links[i], 'link': top_news_links[i], 'title': top_news_titles[i]}
        all_news.append(item)

    # 普通链接新闻
    normal_news_links = html.xpath("//div[@class='newslistcon']/div[@class='listleft']/ul[@class='listtextul']/li/a/@href")
    normal_news_title = html.xpath("//div[@class='newslistcon']/div[@class='listleft']/ul[@class='listtextul']/li/a/text()")
    normal_news_date = html.xpath("//div[@class='newslistcon']/div[@class='listleft']/ul[@class='listtextul']//span[@class='floatright']/text()")
    for i in range(len(normal_news_links)):
        news_publish_date = normal_news_date[i][1:-1]
        item = {'link': normal_news_links[i], 'title': normal_news_title[i], 'date': news_publish_date}
        all_news.append(item)


    # 将链接存进数据库
    gdutschoolnew_all_link = set(db.session.query(GdutSchoolnew.link).all())
    gdutschoolnew_all_tmp = set()
    for line in gdutschoolnew_all_link:
        gdutschoolnew_all_tmp.add(line[0])
    gdutschoolnew_all_link = gdutschoolnew_all_tmp

    for item in all_news:
        if item['link'] not in gdutschoolnew_all_link:
            # 有图片顶部新闻是不带日期的, 而没图片的是带日期的.
            if item.__contains__('src'):
                sql_insert = GdutSchoolnew(link=item['link'], title=item['title'], src=item['src'])
                db.session.add(sql_insert)
                db.session.commit()
            else:
                sql_insert = GdutSchoolnew(link=item['link'], title=item['title'], date=item['date'])
                db.session.add(sql_insert)
                db.session.commit()
            gdutschoolnew_all_link.add(item['link'])

    return all_news