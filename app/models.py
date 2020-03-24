# coding: utf-8
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class BannerTbl(db.Model):
    __tablename__ = 'banner_tbl'

    id = db.Column(db.Integer, primary_key=True)
    banner_image = db.Column(db.String(2083), nullable=False)



class DigitalmagazineTbl(db.Model):
    __tablename__ = 'digitalmagazine_tbl'

    id = db.Column(db.Integer, primary_key=True)
    show_more_href = db.Column(db.String, nullable=False)
    image = db.Column(db.String(2083), nullable=False)
    image_href = db.Column(db.String(2083), nullable=False)



class GraduatepeopleTbl(db.Model):
    __tablename__ = 'graduatepeople_tbl'

    id = db.Column(db.Integer, primary_key=True)
    show_more_href = db.Column(db.String, nullable=False)
    new_title = db.Column(db.String(2083), nullable=False)
    new_href = db.Column(db.String(2083), nullable=False)



class HistoryTbl(db.Model):
    __tablename__ = 'history_tbl'

    id = db.Column(db.Integer, primary_key=True)
    show_more_href = db.Column(db.String, nullable=False)
    new_title = db.Column(db.String(2083), nullable=False)
    new_href = db.Column(db.String(2083), nullable=False)



class HtmlTbl(db.Model):
    __tablename__ = 'html_tbl'

    id = db.Column(db.Integer, primary_key=True)
    html_source_code = db.Column(db.String)



class HumanitiescampusTbl(db.Model):
    __tablename__ = 'humanitiescampus_tbl'

    id = db.Column(db.Integer, primary_key=True)
    professor_show_more_href = db.Column(db.String(2083), nullable=False)
    professor_head_news_image = db.Column(db.String(2083), nullable=False)
    professor_head_news_href = db.Column(db.String(2083), nullable=False)
    professor_head_news_title = db.Column(db.String, nullable=False)
    professor_head_news_profile = db.Column(db.String(2083), nullable=False)
    professor_head_news_profile_see_more = db.Column(db.String, nullable=False)
    professor_sub_news_href = db.Column(db.String(2083), nullable=False)
    professor_sub_news_title = db.Column(db.String, nullable=False)
    student_show_more_href = db.Column(db.String(2083), nullable=False)
    student_head_news_image = db.Column(db.String(2083), nullable=False)
    student_head_news_href = db.Column(db.String(2083), nullable=False)
    student_head_news_title = db.Column(db.String, nullable=False)
    student_head_news_profile = db.Column(db.String, nullable=False)
    student_head_news_profile_see_more = db.Column(db.String(2083), nullable=False)
    student_sub_news_href = db.Column(db.String(2083), nullable=False)
    student_sub_news_title = db.Column(db.String, nullable=False)



class MediagongdaTbl(db.Model):
    __tablename__ = 'mediagongda_tbl'

    id = db.Column(db.Integer, primary_key=True)
    paper_show_more_href = db.Column(db.String(2083), nullable=False)
    paper_sub_news_href = db.Column(db.String(2083), nullable=False)
    paper_sub_news_title = db.Column(db.String(2083), nullable=False)
    media_show_more_href = db.Column(db.String(2083), nullable=False)
    media_sub_news_href = db.Column(db.String(2083), nullable=False)
    media_sub_news_image = db.Column(db.String(2083), nullable=False)
    media_sub_news_title = db.Column(db.String(2083), nullable=False)
    media_sub_news_playtime = db.Column(db.String(2083), nullable=False)
    media_sub_news_date = db.Column(db.String(2083), nullable=False)



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



class StudyplacesTbl(db.Model):
    __tablename__ = 'studyplaces_tbl'

    id = db.Column(db.Integer, primary_key=True)
    higher_edu_perspective_show_more_href = db.Column(db.String, nullable=False)
    higher_edu_perspective_head_news_image = db.Column(db.String(2083), nullable=False)
    higher_edu_perspective_head_news_href = db.Column(db.String(2083), nullable=False)
    higher_edu_perspective_head_news_title = db.Column(db.String, nullable=False)
    higher_edu_perspective_head_news_profile = db.Column(db.String(2083), nullable=False)
    higher_edu_perspective_head_news_profile_see_more = db.Column(db.String, nullable=False)
    higher_edu_perspective_sub_news_href = db.Column(db.String(2083), nullable=False)
    higher_edu_perspective_sub_news_title = db.Column(db.String, nullable=False)
    window_politics_show_more_href = db.Column(db.String(2083), nullable=False)
    window_politics_head_news_image = db.Column(db.String(2083), nullable=False)
    window_politics_head_news_href = db.Column(db.String(2083), nullable=False)
    window_politics_head_news_title = db.Column(db.String, nullable=False)
    window_politics_head_news_profile = db.Column(db.String(2083), nullable=False)
    window_politics_head_news_profile_see_more = db.Column(db.String, nullable=False)
    window_politics_sub_news_href = db.Column(db.String(2083), nullable=False)
    window_politics_sub_news_title = db.Column(db.String, nullable=False)



class TopnewsTbl(db.Model):
    __tablename__ = 'topnews_tbl'

    id = db.Column(db.Integer, primary_key=True)
    topnews_title = db.Column(db.String(2083), nullable=False)
    topnews_href = db.Column(db.String(2083), nullable=False)
