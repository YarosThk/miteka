from myapp import db
from datetime import datetime


class Books(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(60), unique = True, nullable = False)
    author = db.Column(db.String(40), unique = True, nullable = False)
    description = db.Column(db.String(250), unique = True, nullable = False)
    cover = db.Column(db.String(40), unique = True, default = 'default.jpeg')
    pages_total = db.Column(db.Integer, unique = False, nullable = False)
    pages_read = db.Column(db.Integer, unique = False, default = 0)
    date_added = db.Column(db.Integer, unique = False, default = datetime.today)
    annotations = db.relationship("Notes", cascade="all, delete, delete-orphan",
                                    backref = "book", lazy = True)


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    chapter_name = db.Column(db.String(60), nullable = False)
    page_from = db.Column(db.Integer, unique = False)
    page_to = db.Column(db.Integer, unique = False)
    ideas = db.Column(db.Text(), unique = False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable = False)
