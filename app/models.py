from . import db


class HomePage(db.Model):
    __tablename__ = 'home_page'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    link = db.Column(db.String)
