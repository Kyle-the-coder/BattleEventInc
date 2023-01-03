from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt
from flask import flash
from flask_app.controllers.events import Events


class Entry:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.dance_name = data['dance_name']
        self.dance_style = data['dance_style']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.event_id = data['event_id']

    @classmethod
    def create_entry(cls, data):
        query = 'INSERT INTO battle_entries (event_id, first_name, last_name, dance_name, dance_style) VALUES (%(event_id)s, %(first_name)s, %(last_name)s, %(dance_name)s, %(dance_style)s);'
        return connectToMySQL('battle_db').query_db(query, data)


    @classmethod
    def get_all_join_entries(cls, data):
        query = "SELECT * FROM battle_entries JOIN events ON events.id = battle_entries.event_id WHERE events.id = %(id)s;"
        results = connectToMySQL('battle_db').query_db(query, data)
    
        events = []
        for result in results:
            event = cls(result)

            entry_data = {
                **result,
                'id' : result['event_id'],
                'created_at' : result['created_at'],
                'updated_at' : result['updated_at']
            }

            creator = Events(entry_data)
            event.creator = creator
            events.append(event)

        return events


    @classmethod
    def get_one_by_id(cls, data):
        query = 'SELECT * FROM battle_entries WHERE id = %(id)s;'
        results = connectToMySQL('battle_db').query_db(query, data)
        print("results of results is " , results[0])

        if not results or len(results) < 1:
            return False
        else:
            return cls(results[0])