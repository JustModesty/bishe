# from sqlalchemy import Column, Integer, MetaData, String, Text
# # from sqlalchemy import *
# from sqlalchemy.ext.declarative import declarative_base
# # from . import db
#
# Base = declarative_base()
# metadata = Base.metadata
#
#
#
# class BannerTbl(Base):
#     __tablename__ = 'banner_tbl'
#
#     id = Column(Integer, primary_key=True)
#     banner_image = Column(String(2083), nullable=False)
#
#
#
# class DigitalmagazineTbl(Base):
#     __tablename__ = 'digitalmagazine_tbl'
#
#     id = Column(Integer, primary_key=True)
#     show_more_href = Column(String, nullable=False)
#     image = Column(String(2083), nullable=False)
#     image_href = Column(String(2083), nullable=False)
#
#
#
# class GraduatepeopleTbl(Base):
#     __tablename__ = 'graduatepeople_tbl'
#
#     id = Column(Integer, primary_key=True)
#     show_more_href = Column(String, nullable=False)
#     new_title = Column(String(2083), nullable=False)
#     new_href = Column(String(2083), nullable=False)
#
#
#
# class HistoryTbl(Base):
#     __tablename__ = 'history_tbl'
#
#     id = Column(Integer, primary_key=True)
#     show_more_href = Column(String, nullable=False)
#     new_title = Column(String(2083), nullable=False)
#     new_href = Column(String(2083), nullable=False)
#
#
#
# class HumanitiescampusTbl(Base):
#     __tablename__ = 'humanitiescampus_tbl'
#
#     id = Column(Integer, primary_key=True)
#     professor_show_more_href = Column(String(2083), nullable=False)
#     professor_head_news_image = Column(String(2083), nullable=False)
#     professor_head_news_href = Column(String(2083), nullable=False)
#     professor_head_news_title = Column(String, nullable=False)
#     professor_head_news_profile = Column(String(2083), nullable=False)
#     professor_head_news_profile_see_more = Column(String, nullable=False)
#     professor_sub_news_href = Column(String(2083), nullable=False)
#     professor_sub_news_title = Column(String, nullable=False)
#     student_show_more_href = Column(String(2083), nullable=False)
#     student_head_news_image = Column(String(2083), nullable=False)
#     student_head_news_href = Column(String(2083), nullable=False)
#     student_head_news_title = Column(String, nullable=False)
#     student_head_news_profile = Column(String, nullable=False)
#     student_head_news_profile_see_more = Column(String(2083), nullable=False)
#     student_sub_news_href = Column(String(2083), nullable=False)
#     student_sub_news_title = Column(String, nullable=False)
#
#
#
# class MediagongdaTbl(Base):
#     __tablename__ = 'mediagongda_tbl'
#
#     id = Column(Integer, primary_key=True)
#     paper_show_more_href = Column(String(2083), nullable=False)
#     paper_sub_news_href = Column(String(2083), nullable=False)
#     paper_sub_news_title = Column(String(2083), nullable=False)
#     media_show_more_href = Column(String(2083), nullable=False)
#     media_sub_news_href = Column(String(2083), nullable=False)
#     media_sub_news_image = Column(String(2083), nullable=False)
#     media_sub_news_title = Column(String(2083), nullable=False)
#     media_sub_news_playtime = Column(String(2083), nullable=False)
#     media_sub_news_date = Column(String(2083), nullable=False)
#
#
#
# class MenuTbl(Base):
#     __tablename__ = 'menu_tbl'
#
#     id = Column(Integer, primary_key=True)
#     menu_href = Column(String(2083), nullable=False)
#     menu_name = Column(String(2083), nullable=False)
#
#
#
# class SchoolmediaTbl(Base):
#     __tablename__ = 'schoolmedia_tbl'
#
#     id = Column(Integer, primary_key=True)
#     weibo_image = Column(String(2083), nullable=False)
#     weibo_href = Column(String(2083), nullable=False)
#     weixin_image = Column(String(2083), nullable=False)
#     weixin_href = Column(String(2083), nullable=False)
#
#
#
# class SchoolnewsTbl(Base):
#     __tablename__ = 'schoolnews_tbl'
#
#     id = Column(Integer, primary_key=True)
#     schoolnews_parent_href = Column(String(2083), nullable=False)
#     schoolnews_parent_title = Column(String(2083), nullable=False)
#     schoolnews_head_news_image = Column(String(2083), nullable=False)
#     schoolnews_head_news_href = Column(String(2083), nullable=False)
#     schoolnews_head_news_title = Column(String(2083), nullable=False)
#     schoolnews_sub_news_href = Column(String(2083), nullable=False)
#     schoolnews_sub_news_title = Column(String(2083), nullable=False)
#
#
#
# class SchoolnewsslidingTbl(Base):
#     __tablename__ = 'schoolnewssliding_tbl'
#
#     id = Column(Integer, primary_key=True)
#     schoolnews_head_news_image = Column(String(2083), nullable=False)
#     schoolnews_head_news_href = Column(String(2083), nullable=False)
#     schoolnews_head_news_title = Column(String(2083), nullable=False)
#
#
#
# class ShijuegongdaTbl(Base):
#     __tablename__ = 'shijuegongda_tbl'
#
#     id = Column(Integer, primary_key=True)
#     shijuegongda_image = Column(String(2083), nullable=False)
#     shijuegongda_href = Column(String(2083), nullable=False)
#
#
#
# class StudyplacesTbl(Base):
#     __tablename__ = 'studyplaces_tbl'
#
#     id = Column(Integer, primary_key=True)
#     higher_edu_perspective_show_more_href = Column(String, nullable=False)
#     higher_edu_perspective_head_news_image = Column(String(2083), nullable=False)
#     higher_edu_perspective_head_news_href = Column(String(2083), nullable=False)
#     higher_edu_perspective_head_news_title = Column(String, nullable=False)
#     higher_edu_perspective_head_news_profile = Column(String(2083), nullable=False)
#     higher_edu_perspective_head_news_profile_see_more = Column(String, nullable=False)
#     higher_edu_perspective_sub_news_href = Column(String(2083), nullable=False)
#     higher_edu_perspective_sub_news_title = Column(String, nullable=False)
#     window_politics_show_more_href = Column(String(2083), nullable=False)
#     window_politics_head_news_image = Column(String(2083), nullable=False)
#     window_politics_head_news_href = Column(String(2083), nullable=False)
#     window_politics_head_news_title = Column(String, nullable=False)
#     window_politics_head_news_profile = Column(String(2083), nullable=False)
#     window_politics_head_news_profile_see_more = Column(String, nullable=False)
#     window_politics_sub_news_href = Column(String(2083), nullable=False)
#     window_politics_sub_news_title = Column(String, nullable=False)
#
#
#
# class TopnewsTbl(Base):
#     __tablename__ = 'topnews_tbl'
#
#     id = Column(Integer, primary_key=True)
#     topnews_title = Column(String(2083), nullable=False)
#     topnews_href = Column(String(2083), nullable=False)
#
#
# class HtmlTbl(Base):
#     __tablename__ = 'html_tbl'
#
#     id = Column(Integer, primary_key=True)
#     html_source_code = Column(Text)



# =========分界线========
from sqlalchemy import Column, Integer, MetaData, String, Text
# from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from . import db

Base = declarative_base()
metadata = Base.metadata



class BannerTbl(db.Model):
    __tablename__ = 'banner_tbl'

    id = Column(Integer, primary_key=True)
    banner_image = Column(String(2083), nullable=False)



class DigitalmagazineTbl(db.Model):
    __tablename__ = 'digitalmagazine_tbl'

    id = Column(Integer, primary_key=True)
    show_more_href = Column(String, nullable=False)
    image = Column(String(2083), nullable=False)
    image_href = Column(String(2083), nullable=False)



class GraduatepeopleTbl(db.Model):
    __tablename__ = 'graduatepeople_tbl'

    id = Column(Integer, primary_key=True)
    show_more_href = Column(String, nullable=False)
    new_title = Column(String(2083), nullable=False)
    new_href = Column(String(2083), nullable=False)



class HistoryTbl(db.Model):
    __tablename__ = 'history_tbl'

    id = Column(Integer, primary_key=True)
    show_more_href = Column(String, nullable=False)
    new_title = Column(String(2083), nullable=False)
    new_href = Column(String(2083), nullable=False)



class HumanitiescampusTbl(db.Model):
    __tablename__ = 'humanitiescampus_tbl'

    id = Column(Integer, primary_key=True)
    professor_show_more_href = Column(String(2083), nullable=False)
    professor_head_news_image = Column(String(2083), nullable=False)
    professor_head_news_href = Column(String(2083), nullable=False)
    professor_head_news_title = Column(String, nullable=False)
    professor_head_news_profile = Column(String(2083), nullable=False)
    professor_head_news_profile_see_more = Column(String, nullable=False)
    professor_sub_news_href = Column(String(2083), nullable=False)
    professor_sub_news_title = Column(String, nullable=False)
    student_show_more_href = Column(String(2083), nullable=False)
    student_head_news_image = Column(String(2083), nullable=False)
    student_head_news_href = Column(String(2083), nullable=False)
    student_head_news_title = Column(String, nullable=False)
    student_head_news_profile = Column(String, nullable=False)
    student_head_news_profile_see_more = Column(String(2083), nullable=False)
    student_sub_news_href = Column(String(2083), nullable=False)
    student_sub_news_title = Column(String, nullable=False)



class MediagongdaTbl(db.Model):
    __tablename__ = 'mediagongda_tbl'

    id = Column(Integer, primary_key=True)
    paper_show_more_href = Column(String(2083), nullable=False)
    paper_sub_news_href = Column(String(2083), nullable=False)
    paper_sub_news_title = Column(String(2083), nullable=False)
    media_show_more_href = Column(String(2083), nullable=False)
    media_sub_news_href = Column(String(2083), nullable=False)
    media_sub_news_image = Column(String(2083), nullable=False)
    media_sub_news_title = Column(String(2083), nullable=False)
    media_sub_news_playtime = Column(String(2083), nullable=False)
    media_sub_news_date = Column(String(2083), nullable=False)



class MenuTbl(db.Model):
    __tablename__ = 'menu_tbl'

    id = Column(Integer, primary_key=True)
    menu_href = Column(String(2083), nullable=False)
    menu_name = Column(String(2083), nullable=False)



class SchoolmediaTbl(db.Model):
    __tablename__ = 'schoolmedia_tbl'

    id = Column(Integer, primary_key=True)
    weibo_image = Column(String(2083), nullable=False)
    weibo_href = Column(String(2083), nullable=False)
    weixin_image = Column(String(2083), nullable=False)
    weixin_href = Column(String(2083), nullable=False)



class SchoolnewsTbl(db.Model):
    __tablename__ = 'schoolnews_tbl'

    id = Column(Integer, primary_key=True)
    schoolnews_parent_href = Column(String(2083), nullable=False)
    schoolnews_parent_title = Column(String(2083), nullable=False)
    schoolnews_head_news_image = Column(String(2083), nullable=False)
    schoolnews_head_news_href = Column(String(2083), nullable=False)
    schoolnews_head_news_title = Column(String(2083), nullable=False)
    schoolnews_sub_news_href = Column(String(2083), nullable=False)
    schoolnews_sub_news_title = Column(String(2083), nullable=False)



class SchoolnewsslidingTbl(db.Model):
    __tablename__ = 'schoolnewssliding_tbl'

    id = Column(Integer, primary_key=True)
    schoolnews_head_news_image = Column(String(2083), nullable=False)
    schoolnews_head_news_href = Column(String(2083), nullable=False)
    schoolnews_head_news_title = Column(String(2083), nullable=False)



class ShijuegongdaTbl(db.Model):
    __tablename__ = 'shijuegongda_tbl'

    id = Column(Integer, primary_key=True)
    shijuegongda_image = Column(String(2083), nullable=False)
    shijuegongda_href = Column(String(2083), nullable=False)



class StudyplacesTbl(db.Model):
    __tablename__ = 'studyplaces_tbl'

    id = Column(Integer, primary_key=True)
    higher_edu_perspective_show_more_href = Column(String, nullable=False)
    higher_edu_perspective_head_news_image = Column(String(2083), nullable=False)
    higher_edu_perspective_head_news_href = Column(String(2083), nullable=False)
    higher_edu_perspective_head_news_title = Column(String, nullable=False)
    higher_edu_perspective_head_news_profile = Column(String(2083), nullable=False)
    higher_edu_perspective_head_news_profile_see_more = Column(String, nullable=False)
    higher_edu_perspective_sub_news_href = Column(String(2083), nullable=False)
    higher_edu_perspective_sub_news_title = Column(String, nullable=False)
    window_politics_show_more_href = Column(String(2083), nullable=False)
    window_politics_head_news_image = Column(String(2083), nullable=False)
    window_politics_head_news_href = Column(String(2083), nullable=False)
    window_politics_head_news_title = Column(String, nullable=False)
    window_politics_head_news_profile = Column(String(2083), nullable=False)
    window_politics_head_news_profile_see_more = Column(String, nullable=False)
    window_politics_sub_news_href = Column(String(2083), nullable=False)
    window_politics_sub_news_title = Column(String, nullable=False)



class TopnewsTbl(db.Model):
    __tablename__ = 'topnews_tbl'

    id = Column(Integer, primary_key=True)
    topnews_title = Column(String(2083), nullable=False)
    topnews_href = Column(String(2083), nullable=False)


class HtmlTbl(db.Model):
    __tablename__ = 'html_tbl'

    id = Column(Integer, primary_key=True)
    html_source_code = Column(Text)
