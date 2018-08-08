"""Models and database functions for Rideshare project."""

from flask_sqlalchemy import SQLAlchemy
# from server import login

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()

##############################################################################
# Model definitions

class User(db.Model):
    """User information."""

    __tablename__ = "users"


    # Log-in information
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    # authenticated = db.Column(db.Boolean, default=False)

    # Profile information
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    user_gender = db.Column(db.String(20), nullable=False)
    user_bio = db.Column(db.String(160), nullable=False)
    user_profile_img = db.Column(db.String(250), nullable=False)
    user_social_media = db.Column(db.String(3000), nullable=False)

    # # Flask-Login attributes
    # def is_active(self):
    #     """True, as all users are active."""
    #     return True

    # def get_id(self):
    #     """Return the email address to satisfy Flask-Login's requirements."""
    #     return self.email

    # def is_authenticated(self):
    #     """Return True if the user is authenticated."""
    #     return self.authenticated

    # def is_anonymous(self):
    #     """False, as anonymous users aren't supported."""
    #     return False

    # def __repr__(self):
    #     """Provide helpful representation when printed."""

    #     return f"<User user_id={self.user_id} email={self.email}>"


class Trip(db.Model):
    """Trip information."""

    __tablename__ = "trips"


    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date_of_trip = db.Column(db.DateTime, nullable=False)
    max_passengers = db.Column(db.Integer, nullable=False)
    num_passengers = db.Column(db.Integer, nullable=False, default=0)
    willing_to_stop = db.Column(db.Boolean, nullable=False)
    trip_cost = db.Column(db.Integer, nullable=False)

    # User as Driver
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # Places
    origin = db.Column(db.String(64), nullable=False)
    destination = db.Column(db.String(64), nullable=False)

    # Back reference to User
    user = db.relationship("User", backref=db.backref("trips", order_by=trip_id))



class UserTrip(db.Model):
    """User (passenger) has joined a trip."""

    __tablename__ = "user_trips"


    user_trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    # Back reference to Trip
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.trip_id'), nullable=False)
    trip = db.relationship("Trip", backref=db.backref("user_trips", order_by=user_trip_id))

    # User as Passenger
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # Back reference to User
    user = db.relationship("User", backref=db.backref("user_trips", order_by=user_trip_id))



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///rideshares'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")

