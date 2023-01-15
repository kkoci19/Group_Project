from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db_name='bookClub'
    def __init__(self,data):
        self.id = data['id'],
        self.first_name = data['first_name'],
        self.last_name = data['last_name'],
        self.email = data['email'],
        self.password = data['password'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls,data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s,  %(email)s, %(password)s );'
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query= 'SELECT * FROM users WHERE users.email = %(email)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if len(results)<1:
            return False
        return results[0]

    @classmethod
    def get_user_by_id(cls, data):
        query= 'SELECT * FROM users WHERE users.id = %(user_id)s;'
        result = connectToMySQL(cls.db_name).query_db(query, data)
        return result[0]

    @classmethod
    def get_logged_user_favored_books(cls, data):
        query = 'SELECT book_id AS id, users.id FROM favorites LEFT JOIN users on favorites.user_id = users.id WHERE user_id = %(user_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        booksFavored = []
        for row in results:
            booksFavored.append(row['id'])
        return booksFavored

    @classmethod
    def get_who_fav_favorited_books(cls, data):
        query = 'SELECT book_id, users.id, users.first_name, users.last_name FROM favorites LEFT JOIN users on users.id = favorites.user_id WHERE book_id = %(book_id)s;'
        results = connectToMySQL(cls.db_name).query_db(query, data)
        who_fav = []
        if results:
            for row in results:
                who_fav.append(row)
            return who_fav
        return who_fav

    @staticmethod
    def validate_user(user):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("*Invalid email address!", 'emailRegistration')
            is_valid = False
        if len(user['first_name']) < 3:
            flash("*Name must be at least 3 characters!", 'name')
            is_valid = False
        if len(user['last_name']) < 3:
            flash("*Last name must be at least 3 characters!", 'last_name')
            is_valid = False
        if len(user['password']) < 8:
            flash("*Password must be at least 8 characters!", 'passwordRegistration')
            is_valid = False
        if user['confirm_password'] != user['password']:
            flash("*Password does not match!", 'passwordConfirm')
            is_valid = False
        return is_valid
