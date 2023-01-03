from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt
from flask import flash
from flask_app.controllers.users import User


class Events:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']
        self.date = data['date']
        self.details = data['details']
        self.price = data['price']
        self.way_to_pay = data['way_to_pay']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']



    @classmethod
    def create_event(cls, data):
        query = 'INSERT INTO events (user_id, name, location, date, details, price, way_to_pay) VALUES (%(user_id)s, %(name)s, %(location)s, %(date)s, %(details)s, %(price)s, %(way_to_pay)s);'
        return connectToMySQL('battle_db').query_db(query, data)

    
    @classmethod
    def get_all_join(cls, data):
        query = "SELECT * FROM events JOIN users ON users.id = events.user_id;"
        results = connectToMySQL('battle_db').query_db(query, data)
    
        events = []
        for result in results:
            event = cls(result)

            user_data = {
                **result,
                'id' : result['user_id'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at']
            }

            creator = User(user_data)
            event.creator = creator
            events.append(event)

        return events

    
    @classmethod
    def get_one_by_id(cls, data):
        query = 'SELECT * FROM events WHERE id = %(id)s;'
        results = connectToMySQL('battle_db').query_db(query, data)
        print("results of results is " , results[0])

        if not results or len(results) < 1:
            return False
        else:
            return cls(results[0])


    @classmethod
    def get_all_join_events(cls, data):
        query = "SELECT * FROM events JOIN users ON users.id = events.user_id WHERE events.id = %(id)s;"
        results = connectToMySQL('battle_db').query_db(query, data)
        print(results)
    
        events = []
        for result in results:
            event = cls(result)

            user_data = {
                **result,
                'id' : result['user_id'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at']
            }

            creator = User(user_data)
            event.creator = creator
            events.append(event)

        return events


    @classmethod
    def get_all_join_users_events(cls, data):
        query = "SELECT * FROM events JOIN users ON users.id = events.user_id WHERE events.user_id = %(id)s;"
        results = connectToMySQL('battle_db').query_db(query, data)
        print("the results are: ", results)
    
        events = []
        for result in results:
            event = cls(result)

            user_data = {
                **result,
                'id' : result['user_id'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at']
            }

            creator = User(user_data)
            event.creator = creator
            events.append(event)

        return events


    @classmethod
    def update_event(cls, data):
        query = "UPDATE events SET name = %(name)s, details = %(details)s, price = %(price)s, way_to_pay = %(way_to_pay)s WHERE id = %(id)s;"
        results = connectToMySQL('battle_db').query_db(query, data)
        return results

    
    @classmethod
    def delete(cls, data):
        print(data)
        query = "DELETE FROM events WHERE id=%(id)s;"
        return connectToMySQL('battle_db').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM events;"

        results = connectToMySQL('battle_db').query_db(query)

        events = []
        for event in results:
            events.append( cls(event) )
        return events

    @staticmethod
    def validate_event(data):
        is_valid=True
        if len(data['name']) < 2:
            flash("name field must be at least 2 characters")
            is_valid=False
        if len(data['details']) < 2:
            flash("details field must be at least 2 characters")
            is_valid=False
        if len(data['price']) < 2:
            flash("price field must filled out")
            is_valid=False
        if len(data['way_to_pay']) < 1:
            flash("Must put a way to pay")
            is_valid=False
    
        return is_valid