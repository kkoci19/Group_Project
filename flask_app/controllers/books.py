from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.book import Book
from flask_app.models.user import User
from flask import flash

@app.route("/books/new")
def fill_book_form():
    if 'user_id' not in session:
        return redirect("/logOut")
    data = {
            'user_id': session['user_id']
    }
    user = User.get_user_by_id(data)
    return render_template("newBook.html", loggedUser = user)

@app.route('/create_book', methods=['POST'])
def createPosition():
    if 'user_id' not in session:
        return redirect('/logOut')

    if not Book.validate_book(request.form):
        flash('Something went wrong!', 'newBook')
        return redirect(request.referrer)

    data = {
        'title' : request.form['title'],
        'description' : request.form['description'],
        'user_id' : session['user_id']
    }
    Book.create_book(data)
    return redirect('/dashboard')

@app.route('/books/<int:id>')
def display_each_book(id):
    if 'user_id' not in session:
        return redirect('/logOut')
    data = {
        'book_id' : id,
        'user_id' : session['user_id']
    }
    book = Book.get_book_by_id(data)
    user = User.get_user_by_id(data)
    users = Book.get_all_book_info(data)
    usersFavoriteBooks = User.get_logged_user_favored_books(data)
    persons = User.get_who_fav_favorited_books(data)
    if not session['user_id'] == book['user_id']:
        return render_template("bookViewer.html", books = book, loggedUser = user, users = users, persons = persons, usersFavoriteBooks = usersFavoriteBooks)
    if book['id'] not in usersFavoriteBooks:
        Book.addFavor(data)
    return render_template("book.html", books = book, loggedUser = user, users = users, persons = persons )

@app.route('/favorite/<int:id>')
def addFavor(id):
    if 'user_id' not in session:
        return redirect('/logOut')
    data = {
        'book_id': id,
        'user_id': session['user_id']
    }
    Book.addFavor(data)
    return redirect(request.referrer)

@app.route('/update_book/<int:id>', methods=['POST'])
def update_book(id):
    if 'user_id' not in session:
        return redirect('/logOut')

    if not Book.validate_update(request.form):
        return redirect(request.referrer)

    data = { 
        'book_id' : id,
        'title' : request.form['title'],
        'description' : request.form['description'],
    }
    book = Book.get_book_by_id(data)
    Book.update_book(data)
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def deleteBook(id):
    if 'user_id' not in session:
        return redirect('/logOut')
    data = {
        'book_id': id,
    }
    book = Book.get_book_by_id(data)
    Book.deleteAllFavorites(data)
    Book.deleteBook(data)
    return redirect('/dashboard')

@app.route('/unFavorite/<int:id>')
def removeFavor(id):
    if 'user_id' not in session:
        return redirect('/logOut')
    data = {
        'book_id': id,
        'user_id': session['user_id']
    }
    Book.removeFavor(data)
    return redirect(request.referrer)
