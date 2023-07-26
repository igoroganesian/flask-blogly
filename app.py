"""Blogly application."""

import os

from flask import Flask, request, render_template, redirect
from models import connect_db, db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", 'postgresql:///blogly')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

debug = DebugToolbarExtension(app)

connect_db(app)

@app.get('/')
def redirect_to_user_list():
    """ Re-directs GETs to root to user list endpoint """

    return redirect('/users')

@app.get('/users')
def display_user_list():
    """ Grabs the list of users and displays them """

    users = User.query.all()

    return render_template('users.html', users=users)

@app.get('/users/new')
def display_add_form():
    """ Returns new user form """

    return render_template('new-user.html')

@app.post('/users/new')
def create_new_user():
    """ Adds new user to db """

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.get('/users/<int:user_id>')
def show_user(user_id):
    """ Display individual user page """

    user = User.query.get(user_id)

    return render_template('user-id.html', user=user)

@app.get('/users/<int:user_id>/edit')
def display_edit_form(user_id):
    """ Display edit user form"""

    user = User.query.get(user_id)

    return render_template('edit-user.html', user=user)

@app.post('/users/<int:user_id>/edit')
def edit_user(user_id):
    """ Edits an existing user and redirect to user list """

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user = User.query.get(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url if image_url else None

    db.session.commit()

    return redirect('/users')

@app.post('/users/<int:user_id>/delete')
def delete_user(user_id):
    """ deletes the specified user and redirect to user list """

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


