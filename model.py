"""Models and database functions for Rideshare project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import date
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

    # Profile information
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20), nullable=False)
    user_gender = db.Column(db.String(20), nullable=False)
    user_bio = db.Column(db.String(160), nullable=False)
    user_profile_img = db.Column(db.String(250), nullable=False)
    user_social_media = db.Column(db.String(3000), nullable=False)
    # phone_number = db.Column(db.Numeric(12), nullable=True)

    def to_json(self):
        """Converts to JSON"""

        return {'user_id': self.user_id,
                'email': self.email,
                'password': self.password,
                'fname': self.fname,
                'lname': self.lname,
                'user_gender': self.user_gender,
                'user_bio': self.user_bio,
                'user_profile_img': self.user_profile_img,
                'user_social_media': self.user_social_media}

class Trip(db.Model):
    """Trip information."""

    __tablename__ = "trips"


    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date_of_trip = db.Column(db.Date, nullable=False)
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

    def to_json(self):
        """Converts to JSON"""

        datetime_str = self.date_of_trip.strftime('%Y-%m-%d')

        return {'trip_id': self.trip_id,
                'date_of_trip': datetime_str,
                'max_passengers': self.max_passengers,
                'num_passengers': self.num_passengers,
                'willing_to_stop': self.willing_to_stop,
                'trip_cost': self.trip_cost,
                'origin': self.origin,
                'destination': self.destination,
                'user_as_driver': self.user_id}

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

    def to_json(self):
        """Converts to JSON"""

        return {'user_trip_id': self.user_trip_id,
                'trip_id': self.trip_id,
                'user_id': self.user_id,
                'date_of_trip': self.trip.date_of_trip,
                'user_fname': self.user.fname,
                'origin': self.trip.origin,
                'destination': self.trip.destination}



##############################################################################
# Helper functions

def connect_to_db(app, db_uri="postgresql:///rideshares"):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

def example_data():
    user = User(fname="Jo",
                lname="Bama",
                email="jo@bama.com",
                user_bio="Friendly person",
                user_gender="Female",
                password="jo@bama.com",
                user_profile_img="https://robohash.org/enimsolutaqui.png?size=50x50&set=set1",
                user_social_media="twitter.com")
    db.session.add(user)
    db.session.commit()

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")

