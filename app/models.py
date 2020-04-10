# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, SmallInteger, String, Text
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class BannerTbl(db.Model):
    __tablename__ = 'banner_tbl'

    id = db.Column(db.Integer, primary_key=True)
    banner_image = db.Column(db.String(2083), nullable=False)



class Book(db.Model):
    __tablename__ = 'book'

    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    delete_time = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(30))
    summary = db.Column(db.String(1000))
    image = db.Column(db.String(50))



class DigitalmagazineTbl(db.Model):
    __tablename__ = 'digitalmagazine_tbl'

    id = db.Column(db.Integer, primary_key=True)
    show_more_href = db.Column(db.String, nullable=False)
    image = db.Column(db.String(2083), nullable=False)
    image_href = db.Column(db.String(2083), nullable=False)



class GdutDetailpage(db.Model):
    __tablename__ = 'gdut_detailpage'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(500), nullable=False)
    jianjie = db.Column(db.String(500))



class GdutDetailpageContent(db.Model):
    __tablename__ = 'gdut_detailpage_content'

    id = db.Column(db.Integer, primary_key=True)
    detail_link = db.Column(db.String(500), nullable=False)
    paragraph = db.Column(db.Text, nullable=False)



class GdutDetailpagePicture(db.Model):
    __tablename__ = 'gdut_detailpage_picture'

    id = db.Column(db.Integer, primary_key=True)
    detail_link = db.Column(db.String(500), nullable=False)
    local_position = db.Column(db.String(500), nullable=False)



class GdutMeitigongda(db.Model):
    __tablename__ = 'gdut_meitigongda'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    src = db.Column(db.String(500))
    date = db.Column(db.String(500))



class GdutRenwenxiaoyuan(db.Model):
    __tablename__ = 'gdut_renwenxiaoyuan'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    src = db.Column(db.String(500))
    date = db.Column(db.String(500))



class GdutSchoolnew(db.Model):
    __tablename__ = 'gdut_schoolnews'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    src = db.Column(db.String(500))
    date = db.Column(db.String(500))



class GdutTupianxinwen(db.Model):
    __tablename__ = 'gdut_tupianxinwen'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    src = db.Column(db.String(500))
    date = db.Column(db.String(500))



class GdutWangshangxiaoshiguan(db.Model):
    __tablename__ = 'gdut_wangshangxiaoshiguan'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    src = db.Column(db.String(500))
    date = db.Column(db.String(500))



class GdutXiaoyoudongtai(db.Model):
    __tablename__ = 'gdut_xiaoyoudongtai'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    src = db.Column(db.String(500))
    date = db.Column(db.String(500))



class GdutXuexiyuandi(db.Model):
    __tablename__ = 'gdut_xuexiyuandi'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    src = db.Column(db.String(500))
    date = db.Column(db.String(500))



class GdutZhuanlanbaodao(db.Model):
    __tablename__ = 'gdut_zhuanlanbaodao'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    src = db.Column(db.String(500))
    date = db.Column(db.String(500))



class GraduatepeopleTbl(db.Model):
    __tablename__ = 'graduatepeople_tbl'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(2083), nullable=False)
    title = db.Column(db.String(2083), nullable=False)



class HasLinkTbl(db.Model):
    __tablename__ = 'has_link_tbl'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(100), nullable=False)



class HistoryTbl(db.Model):
    __tablename__ = 'history_tbl'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(2083), nullable=False)
    title = db.Column(db.String(2083), nullable=False)



class HtmlTbl(db.Model):
    __tablename__ = 'html_tbl'

    id = db.Column(db.Integer, primary_key=True)
    html_source_code = db.Column(db.String)



class HumanityCampusNew(db.Model):
    __tablename__ = 'humanity_campus_news'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(1024), nullable=False)
    title = db.Column(db.String(1024), nullable=False)



class Image(db.Model):
    __tablename__ = 'image'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    _from = db.Column('from', db.Integer, nullable=False)



class LinAuth(db.Model):
    __tablename__ = 'lin_auth'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, nullable=False, info='所属权限组id')
    auth = db.Column(db.String(60), info='权限字段')
    module = db.Column(db.String(50), info='权限的模块')



class LinEvent(db.Model):
    __tablename__ = 'lin_event'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, nullable=False, info='所属权限组id')
    message_events = db.Column(db.String(250), info='信息')



class LinFile(db.Model):
    __tablename__ = 'lin_file'

    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    delete_time = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(500), nullable=False, info='路径')
    type = db.Column(db.SmallInteger, info='1 local，其他表示其他地方')
    name = db.Column(db.String(100), nullable=False, info='名称')
    extension = db.Column(db.String(50), nullable=False, info='后缀')
    size = db.Column(db.Integer, info='大小')
    md5 = db.Column(db.String(40), unique=True, info='图片md5值，防止上传重复图片')



class LinGroup(db.Model):
    __tablename__ = 'lin_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), info='权限组名称')
    info = db.Column(db.String(255), info='权限组描述')



class LinLog(db.Model):
    __tablename__ = 'lin_log'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(450), info='日志信息')
    time = db.Column(db.DateTime, info='日志创建时间')
    user_id = db.Column(db.Integer, nullable=False, info='用户id')
    user_name = db.Column(db.String(20), info='用户当时的昵称')
    status_code = db.Column(db.Integer, info='请求的http返回码')
    method = db.Column(db.String(20), info='请求方法')
    path = db.Column(db.String(50), info='请求路径')
    authority = db.Column(db.String(100), info='访问哪个权限')



class LinPoem(db.Model):
    __tablename__ = 'lin_poem'

    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    delete_time = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False, info='标题')
    author = db.Column(db.String(50), info='作者')
    dynasty = db.Column(db.String(50), info='朝代')
    content = db.Column(db.Text, nullable=False, info='内容，以/来分割每一句，以|来分割宋词的上下片')
    image = db.Column(db.String(255), info='配图')



class LinUser(db.Model):
    __tablename__ = 'lin_user'

    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    delete_time = db.Column(db.DateTime)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False, unique=True, info='用户名')
    nickname = db.Column(db.String(24), unique=True, info='昵称')
    avatar = db.Column(db.String(255), info='头像url')
    admin = db.Column(db.SmallInteger, nullable=False, info='是否为超级管理员 ;  1 -> 普通用户 |  2 -> 超级管理员')
    active = db.Column(db.SmallInteger, nullable=False, info='当前用户是否为激活状态，非激活状态默认失去用户权限 ; 1 -> 激活 | 2 -> 非激活')
    email = db.Column(db.String(100), unique=True, info='电子邮箱')
    group_id = db.Column(db.Integer, info='用户所属的权限组id')
    password = db.Column(db.String(100), info='密码')



class MenuTbl(db.Model):
    __tablename__ = 'menu_tbl'

    id = db.Column(db.Integer, primary_key=True)
    menu_href = db.Column(db.String(2083), nullable=False)
    menu_name = db.Column(db.String(2083), nullable=False)



class MoreButtonTbl(db.Model):
    __tablename__ = 'more_button_tbl'

    id = db.Column(db.Integer, primary_key=True)
    paper_show_more_href = db.Column(db.String(1000), nullable=False)
    media_show_more_href = db.Column(db.String(1000), nullable=False)
    professor_show_more_href = db.Column(db.String(1000), nullable=False)
    student_show_more_href = db.Column(db.String(1000), nullable=False)
    higher_edu_perspective_show_more_href = db.Column(db.String(1000), nullable=False)
    window_politics_show_more_href = db.Column(db.String(1000), nullable=False)
    digitalmagazine_show_more_href = db.Column(db.String(1000), nullable=False)
    special_column_report_show_more_href = db.Column(db.String(1000), nullable=False)
    graduate_people_show_more_href = db.Column(db.String(1000), nullable=False)
    history_show_more_href = db.Column(db.String(1000), nullable=False)



class SchoolmediaTbl(db.Model):
    __tablename__ = 'schoolmedia_tbl'

    id = db.Column(db.Integer, primary_key=True)
    weibo_image = db.Column(db.String(2083), nullable=False)
    weibo_href = db.Column(db.String(2083), nullable=False)
    weixin_image = db.Column(db.String(2083), nullable=False)
    weixin_href = db.Column(db.String(2083), nullable=False)



class SchoolnewsTbl(db.Model):
    __tablename__ = 'schoolnews_tbl'

    id = db.Column(db.Integer, primary_key=True)
    schoolnews_parent_href = db.Column(db.String(2083), nullable=False)
    schoolnews_parent_title = db.Column(db.String(2083), nullable=False)
    schoolnews_head_news_image = db.Column(db.String(2083), nullable=False)
    schoolnews_head_news_href = db.Column(db.String(2083), nullable=False)
    schoolnews_head_news_title = db.Column(db.String(2083), nullable=False)



class SchoolnewsslidingTbl(db.Model):
    __tablename__ = 'schoolnewssliding_tbl'

    id = db.Column(db.Integer, primary_key=True)
    schoolnews_head_news_image = db.Column(db.String(2083), nullable=False)
    schoolnews_head_news_href = db.Column(db.String(2083), nullable=False)
    schoolnews_head_news_title = db.Column(db.String(2083), nullable=False)



class SchoolnewssubnewsTbl(db.Model):
    __tablename__ = 'schoolnewssubnews_tbl'

    id = db.Column(db.Integer, primary_key=True)
    schoolnews_sub_news_href = db.Column(db.String(2083), nullable=False)
    schoolnews_sub_news_title = db.Column(db.String(2083), nullable=False)



class ShijuegongdaTbl(db.Model):
    __tablename__ = 'shijuegongda_tbl'

    id = db.Column(db.Integer, primary_key=True)
    shijuegongda_image = db.Column(db.String(2083), nullable=False)
    shijuegongda_href = db.Column(db.String(2083), nullable=False)



class StudyplacesNewsTbl(db.Model):
    __tablename__ = 'studyplaces_news_tbl'

    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(2083), nullable=False)
    title = db.Column(db.String(2083), nullable=False)



class TopnewsTbl(db.Model):
    __tablename__ = 'topnews_tbl'

    id = db.Column(db.Integer, primary_key=True)
    topnews_title = db.Column(db.String(2083), nullable=False)
    topnews_href = db.Column(db.String(2083), nullable=False)



class Zhimeihui(db.Model):
    __tablename__ = 'zhimeihui'

    id = db.Column(db.Integer, primary_key=True)
    paper_sub_news_href = db.Column(db.String(2083), nullable=False)
    paper_sub_news_title = db.Column(db.String(2083), nullable=False)
