from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt
from flask import flash
from flask_app.controllers.events import Events


class Bracket:
    def __init__(self, data):
        self.id = data['id']
        self.dancers = data['dancers']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create_bracket(cls, data):
        query = 'INSERT INTO bracket (dancers) VALUES (%(dancers)s);'
        return connectToMySQL('battle_db').query_db(query, data)