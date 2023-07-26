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