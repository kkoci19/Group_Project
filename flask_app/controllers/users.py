from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.book import Book
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/register')
def devRegisterPage():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('register.html')

@app.route('/create_user', methods=['POST'])
def create_user():
    if 'user_id' in session:
        return redirect('/register')

    if not User.validate_user(request.form):
        flash('Something went wrong!', 'userRegistration')
        return redirect(request.referrer)

    if User.get_user_by_email(request.form):
        flash('This email already exists!', 'emailRegistration')
        return redirect(request.referrer)

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
    }
    User.create_user(data)
    flash('Succesfull Registration!', 'userRegistrationSuccessful')
    return redirect('/logIn')

@app.route('/enter_userDashboard', methods=['POST'])
def userDashboard():
    if 'user_id' in session:
        return redirect('/logIn')

    data = {
        'email': request.form['email']
    }

    if len(request.form['email'])<1:
        flash('*Email is required to login!', 'emailLogin')
        return redirect(request.referrer)

    if not User.get_user_by_email(data):
        flash('*This email does not exist!', 'emailLogin')
        return redirect(request.referrer)

    user = User.get_user_by_email(data)

    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("*Invalid Password!", 'passwordLogin')
        return redirect(request.referrer)

    session['user_id'] = user['id']
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        data = {
            'user_id': session['user_id']
        }
        user = User.get_user_by_id(data)
        books = Book.getAllBooks(data)
        usersFavoriteBooks = User.get_logged_user_favored_books(data)
        return render_template('dashboard.html', loggedUser = user, books = books, usersFavoriteBooks = usersFavoriteBooks)
    return redirect('/logOut')


@app.route('/logIn')
def loginPage():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/logOut')
def logout():
    session.clear()
    return redirect('/logIn')

