"""Models for Blogly."""
class User(db.Model):

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
        db.String(50),
        nullable=True
    )