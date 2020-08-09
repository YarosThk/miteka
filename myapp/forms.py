from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired


class BookForm(FlaskForm):
    # we can remove placeholders from here and put them in the html
    # same way as we did with UpdateBook, this way we don't mix
    # structural code with style.
    title = StringField("Title", validators=[Length(min=1, max=60),
                                             DataRequired()], render_kw={"placeholder": "Book title"})
    author = StringField("Author", validators=[Length(min=1, max=40),
                                               DataRequired()], render_kw={"placeholder": "Author's name"})
    description = TextAreaField("Description", validators=[Length(min=1, max=250)],
                                render_kw={"placeholder": "Book's description"})
    #passed Id for the Label tag in AddBook to identify the cover field in the class
    cover = FileField("Book cover", validators=[FileAllowed(['jpg', "jpeg"])], id="UploadLabel")
    pages_total = IntegerField("Pages", validators=[InputRequired()], render_kw={"placeholder": "Number of pages"})
    pages_read = IntegerField("Pages read", validators=[InputRequired()], render_kw={"placeholder": "Pages read"})
    submit = SubmitField("Add book")


class UpdateBook(FlaskForm):
    title = StringField("Title", validators=[Length(min=1, max=60), DataRequired()])
    author = StringField("Author", validators=[Length(min=1, max=40), DataRequired()])
    description = TextAreaField("Description", validators=[Length(min=1, max=250)])
    #passed Id for the Label tag in SubmitBook to identify the cover field in the class
    cover = FileField("Update book's cover", validators=[FileAllowed(['jpg'])], id="UpdateCoverLabel")
    pages_total = IntegerField("Pages", validators=[InputRequired()])
    pages_read = IntegerField("Pages read", validators=[InputRequired()])
    update = SubmitField("Update book")


class AddNote(FlaskForm):
    chapter = StringField("Chapter", validators=[Length(min=1, max=60), DataRequired()])
    from_page = StringField()
    to_page = StringField()
    ideas = TextAreaField("Notes", validators=[Length(min=1, max=2000), DataRequired()])
    add_note = SubmitField("Add note")
