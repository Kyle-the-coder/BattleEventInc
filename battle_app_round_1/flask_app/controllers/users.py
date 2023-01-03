from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models.user import User
from flask_app import bcrypt

@app.route('/')
def index():
    return render_template('reg.html')


@app.route('/register', methods=["POST"])
def register():

    if not User.validate_password(request.form):
        return redirect('/')

    hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'dance_name': request.form['dance_name'],
        'email' : request.form['email'],
        'password' : hash
    }
    print(data)
    User.create_user(data)
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    if not User.validate_login(request.form):
        return redirect('/')

    user_found = User.get_one_by_email(request.form)
    print(user_found)

    session['uid'] = user_found.id
    session['first_name'] = user_found.first_name
    session['last_name'] = user_found.last_name
    session['user_id'] = user_found.id
    

    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

