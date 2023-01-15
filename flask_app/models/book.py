from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Book:
    db_name='bookClub'
    def __init__(self,data):
        self.id = data['id'],
        self.title = data['title'],
        self.description = data['description'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    @classmethod
    def create_book(cls,data):
        query = 'INSERT INTO books (title, description, user_id) VALUES ( %(title)s, %(description)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def getAllBooks(cls,data):
        query= 'SELECT books.id, books.title, users.id AS user_id, users.first_name, users.last_name FROM books LEFT JOIN users ON users.id = books.user_id LEFT JOIN favorites ON favorites.book_id = books.id GROUP BY books.id;'
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        books= []
        if results:
            for row in results:
                books.append(row)
            return books
        return books

    @classmethod
    def get_book_by_id(cls, data):
        query= 'SELECT * FROM books WHERE books.id = %(book_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        return results[0]

    @classmethod
    def get_all_book_info(cls, data):
        query= 'SELECT users.id, first_name, last_name, books.id as book_id, books.created_at, books.updated_at FROM books LEFT JOIN users on users.id = books.user_id LEFT JOIN favorites on favorites.book_id = books.id WHERE books.id = %(book_id)s GROUP BY users.id;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        who_fav = []
        if results:
            for row in results:
                who_fav.append(row)
            return who_fav
        return who_fav

    @classmethod
    def addFavor(cls, data):
        query= 'INSERT INTO favorites (book_id, user_id) VALUES ( %(book_id)s, %(user_id)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def update_book(cls, data):
        query = 'UPDATE books SET title = %(title)s, description = %(description)s WHERE books.id = %(book_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def deleteBook(cls, data):
        query= 'DELETE FROM books WHERE books.id = %(book_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def deleteAllFavorites(cls, data):
        query= 'DELETE FROM favorites WHERE favorites.book_id = %(book_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def removeFavor(cls, data):
        query= 'DELETE FROM favorites WHERE book_id = %(book_id)s and user_id = %(user_id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @staticmethod
    def validate_book(book):
        is_valid = True
        if len(book['title']) < 5:
            flash("*Title is required!", 'title')
            is_valid = False
        if len(book['description']) < 5:
            flash("*Description must be at least 5 characters!", 'description')
            is_valid = False
        return is_valid

    @staticmethod
    def validate_update(update):
        is_valid = True
        if len(update['title']) < 3:
            flash("*Title is required!", 'update_title')
            is_valid = False
        if len(update['description']) < 5:
            flash("*Description must be at least 5 characters.", 'update_description')
            is_valid = False
        return is_valid

