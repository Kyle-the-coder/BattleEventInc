from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.dance_name = data['dance_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    @classmethod
    def create_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, dance_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(dance_name)s, %(email)s, %(password)s)'
        return connectToMySQL('battle_db').query_db(query, data)

    
    @classmethod
    def get_all_user(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL('battle_db').query_db(query)
        users =[]
        for dict in results:
            user = cls(dict)
            users.append(user)
        return users


    
    @classmethod
    def get_one_by_name(cls, data):
        query = 'SELECT * FROM users WHERE first_name = %(first_name)s'
        results = connectToMySQL('battle_db').query_db(query, data)

        if not results or len(results) < 1:
            return False
        else:
            return cls(results[0])

        

    
    @classmethod
    def get_one_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        results = connectToMySQL('battle_db').query_db(query, data)

        if not results or len(results) < 1:
            return False
        else:
            return cls(results[0])

    
    @classmethod
    def get_one_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s'
        results = connectToMySQL('battle_db').query_db(query, data)
        print(results)

        if not results or len(results) < 1:
            return False
        else:
            return cls(results[0])


    
    @staticmethod
    def validate_login(data):
        is_valid = True
        print(data)

        user_found = User.get_one_by_email(data)

        if user_found:
            if not bcrypt.check_password_hash(user_found.password, data['password']):
                is_valid=False
        else:
            is_valid=False

        if not is_valid:
            flash('Invalid login')
        
        return is_valid




    @staticmethod
    def validate_password(data):
        is_valid = True

        if data['password'] != data['confirm_password']:
            is_valid = False
            flash("Passwords must match")

        if User.get_one_by_email(data):
            is_valid = False
            flash('Email already registered')

        if len(data['first_name']) < 2 and len(data['last_name']) < 2:
            flash('First name and Last name must be at least 3 characters')
            is_valid = False

        if len(data['password']) < 8:
            flash('Password must be at least 8 characters')
            is_valid = False

        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False

        return is_valid