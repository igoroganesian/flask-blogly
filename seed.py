"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
# An alternative if you don't want to drop
# and recreate your tables:
# Pet.query.delete()

# Add pets
jason = User(first_name='Jason', last_name="Johnson")
igor = User(first_name='Igor', last_name="Oganesian")

# Add new objects to session, so they'll persist
db.session.add(jason)
db.session.add(igor)

# Commit--otherwise, this never gets saved!
db.session.commit()

