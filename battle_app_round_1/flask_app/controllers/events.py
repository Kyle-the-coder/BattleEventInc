from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.event import Events
from flask_app.models.battle_entry import Entry
from flask_app.models.user import User
from flask_app import bcrypt


@app.route("/create_events_page")
def create_recipe_page():
    return render_template('create_event.html')



@app.route('/create_event', methods=["POST"])
def create_sighting():
    print(request.form)

    if not Events.validate_event(request.form):
        return redirect('/create_events_page')

    data = {
        'name' : request.form['name'],
        "location" : request.form['location'],
        "date" : request.form['date'],
        'details' : request.form['details'],
        'price' : request.form['price'],
        'way_to_pay' : request.form['way_to_pay'],
        'user_id' : session['uid']
    }
    print(data)
    Events.create_event(data)
    return redirect('/dashboard')
    



@app.route('/dashboard')
def dashboard():
    if not 'uid' in session:
        flash("you must log in")
        return redirect('/')
    user_data = {
        'user_id' : session['user_id']
    }
    dance_data = {
        'id' : session['user_id']
    }
    
    

    events = Events.get_all_join(user_data)
    dance_name = User.get_one_by_id(dance_data)
    


    return render_template('dashboard.html', events = events, dance_name=dance_name)
        
    


@app.route('/view_event/<int:event_id>')
def view_event(event_id):
    user_data = {
        'id' : event_id,
    }
    events = Events.get_all_join_events(user_data)
    entries = Entry.get_all_join_entries(user_data)
    return render_template('display_one_event.html', events = events, entries = entries)
        


@app.route('/edit_event_page/<int:event_id>')
def edit_event_page(event_id):

    user_data = {
        'id' : event_id,
    }
    events = Events.get_one_by_id(user_data)
    print(events)
    return render_template('edit_event.html', events = events)
        


@app.route('/edit_event/<int:event_id>', methods = ["POST"])
def edit_sighting(event_id):

    if not Events.validate_event(request.form):
        return redirect(f'/edit_sighting_page/{event_id}')

    event_data = {
        'id' : event_id,
        'name' : request.form['name'],
        'location' : request.form['location'],
        'details' : request.form['details'],
        'price' : request.form['price'],
        'way_to_pay' : request.form['way_to_pay'],
    }
    Events.update_event(event_data)
    return redirect('/dashboard')



@app.route('/delete/<int:num>')
def delete(num):
    deleteData = {
        'id' : num
    }
    Events.delete(deleteData)
    return redirect('/dashboard')