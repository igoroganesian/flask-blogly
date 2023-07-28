"""Seed file to make sample data for pets db."""

from models import User, Post, Tag, db
from app import app

# Create all tables
#TODO: specify order?

db.drop_all()
db.create_all()

# If table isn't empty, empty it
# An alternative if you don't want to drop
# and recreate your tables:

# Add users
jason = User(first_name='Jason', last_name="Johnson")
igor = User(first_name='Igor', last_name="Oganesian")

# Add new objects to session, so they'll persist
db.session.add(jason)
db.session.add(igor)

# Commit--otherwise, this never gets saved!
db.session.commit()

# Add posts
post1 = Post(title='Title', content='Post contentasdfasdfasdf', user_id=jason.id)
post2 = Post(title='Title', content='Post contentasdfasdfasdf', user_id=jason.id)
post3 = Post(title='Title', content='Post contentasdfasdfasdf', user_id=jason.id)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)

db.session.commit()

# tag1 = Tag(name='tagOne')
# tag2 = Tag(name='tagTwo')
# tag3 = Tag(name='tagThree')

# db.session.add(post1)
# db.session.add(post1)
# db.session.add(post1)
