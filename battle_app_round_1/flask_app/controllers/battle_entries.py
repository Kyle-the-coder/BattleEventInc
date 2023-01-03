from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models.battle_entry import Entry
from flask_app.models.event import Events
from flask_app.models.bracket import Bracket
from flask_app import bcrypt

@app.route('/enter_battle_page')
def entry():

    events = Events.get_all()
    return render_template('battle_sign_up.html', events = events)




@app.route('/create_entry', methods=["POST"])
def create_entry_1():
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'dance_name' : request.form['dance_name'],
        'dance_style' : request.form['dance_style'],
        'event_id' : request.form['event_id']
    }
    Entry.create_entry(data)
    print(data)
    return redirect('/dashboard')

@app.route('/host_page')
def host_page():
    user_data = {
        'id' : session['user_id']
    }
    events = Events.get_all_join_users_events(user_data)

    return render_template('host_page.html', events = events)

@app.route('/bracket_page/<int:event_id>')
def bracket_page(event_id):
    user_data = {
        'id' : event_id,
    }
    entries = Entry.get_all_join_entries(user_data)
    events = Events.get_all_join_events(user_data)
    
    return render_template('bracket.html', events = events, entries=entries)

@app.route('/generate_bracket/<int:event_id>', methods=["POST"])
def generate_bracket(event_id):
    data={
        'dancers' : request.form['enter']
    }
    Bracket.create_bracket(data)
    
    return redirect(f'/bracket_page/{event_id}')