from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://rithm-students-media.s3.amazonaws.com/CACHE/images/user_photos/joel/67987019-1bc4-485b-b4a8-5bca9c2381d1-5281391517_21c58b50e0_o/18697a97aac35b539bf6d017aa499f0d.jpg"

def connect_db(app):
    """Connect to database."""
    app.app_context().push()
    db.app = app
    db.init_app(app)

class User(db.Model):
    """ A user creates posts """

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
        )

    first_name = db.Column(
        db.String(50),
        nullable=False,
    )

    last_name = db.Column(
        db.String(50),
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        nullable=True
    )

    posts = db.relationship('Post', backref='user')

class Post(db.Model):
    """ TODO: Doc string for posts """

    __tablename__ = "posts"

    # user = The user who is associated with this post

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
        )

    title = db.Column(
        db.String(50),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone = True),
        nullable = False,
        default = db.func.now()
    )

    user_id = db.Column(
        db.Integer(),
        db.ForeignKey('users.id'),
        nullable = False
    )