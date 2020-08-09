from flask import render_template,request, redirect, url_for, flash, Blueprint, current_app, jsonify
from myapp import db
from myapp.models import Books, Notes
from myapp.forms import BookForm, UpdateBook, AddNote
from myapp.utils import save_cover, delete_cover

main = Blueprint('main',__name__)


@main.route("/", methods = ['GET', 'POST'])
@main.route("/home", methods = ['GET', 'POST'])
def home():
    book_form = BookForm()
    book_cover = None
    if book_form.validate_on_submit():
        if book_form.cover.data:
            book_cover = save_cover(book_form.cover.data)

        book = Books(title = book_form.title.data, author = book_form.author.data,
                        description = book_form.description.data,
                        cover = book_cover,
                        pages_total = book_form.pages_total.data,
                        pages_read = book_form.pages_total.data)

        db.session.add(book)
        db.session.commit()
        flash('Added successfully!', 'success')
        return redirect(url_for('main.home'))

    return render_template("home.html", title = "Welcome!", form = book_form)


#route to query all my books
@main.route("/my_books", methods = ['GET', 'POST'])
def book_view():
    all_books = Books.query.all()
    return render_template("library.html", title = "My Library", library_content = all_books)



#route to delete the book entiries.
#this is a route that will receive AJAX request (req dict object)
#takes that book_ID from that request to query our DB.
@main.route("/my_books/delete/book", methods = ['POST'])
def delete_book():
    book_deletion = Books.query.filter_by(id = request.form['book_ID']).first() #this request comes from JS

    if book_deletion.cover != "default.jpeg":
        delete_cover(book_deletion.cover)

    db.session.delete(book_deletion)
    db.session.commit()
    flash('You have deleted the book!', 'success')
    return jsonify({"result" : "success"})



#gets called by the search button in the nav bar
#executes sql query LIKE %#%
@main.route("/search", methods = ["POST"])
def search_book():
    book_search = Books.query.filter(Books.title.like("%" + request.form["book_title"] + "%")).first()

    if book_search != None:
        return redirect(url_for("main.edit_book", book_id = book_search.id))
    else:
        flash('Title does not exist!', 'danger')
        return redirect(url_for("main.home"))



@main.route("/my_books/edit/<book_id>", methods = ['POST', 'GET'])
def edit_book(book_id):
    queried_book = Books.query.get_or_404(book_id)
    queried_notes = Notes.query.filter(Notes.book_id == book_id).order_by("page_from").all()
    #pass the queried book to the update book form, fillin in the data
    update_form = UpdateBook(obj = queried_book)
    add_notes = AddNote()


    if update_form.update.data and update_form.validate_on_submit():

        if update_form.cover.data != queried_book.cover:
            if queried_book.cover != "default.jpeg":
                delete_cover(queried_book.cover)
            cover_file = save_cover(update_form.cover.data)
            queried_book.cover = cover_file

        queried_book.title = update_form.title.data
        queried_book.author = update_form.author.data
        queried_book.description = update_form.description.data
        queried_book.pages_total = update_form.pages_total.data
        queried_book.pages_read = update_form.pages_read.data
        db.session.commit()
        return redirect(url_for("main.edit_book", book_id = book_id))


    elif add_notes.add_note.data and add_notes.validate_on_submit():
        note = Notes(chapter_name = add_notes.chapter.data , page_from = add_notes.from_page.data,
                        page_to = add_notes.to_page.data, ideas = add_notes.ideas.data, book_id = book_id)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for("main.edit_book", book_id = book_id))

    #executed with View button in the library
    #view button calls edit_book and passes the book_id parameter
    #probably a really weird way to implement that
    elif request.method == "GET":
        return render_template("book_details.html", book = queried_book, book_notes = queried_notes,
                            update_form = update_form, notes_form = add_notes)

    return render_template("book_details.html", book = queried_book, book_notes = queried_notes,
                        update_form = update_form, notes_form = add_notes)



#this is a route that will receive AJAX request (req dict object)
#we take that note_ID from that AJX request to query our DB.
@main.route("/my_books/edit/note", methods = ['POST'])
def delete_note():
    #get_or_404 may be more flexible than filter_by
    note_deletion = Notes.query.get_or_404(request.form['note_ID'])
    db.session.delete(note_deletion)
    db.session.commit()
    return jsonify({"result" : "success"})
