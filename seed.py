"""Utility file to seed user and trip information."""

from sqlalchemy import func
from model import connect_to_db, db
from server import app
from random import choice


# def set_val_user_id(): # pragma: no cover
#     """Set value for the next user_id after seeding database."""
#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()

#     max_id = int(result[0])
#     print(max_id)

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


# def set_val_trip_id(): # pragma: no cover
#     """Set value for the next trip after seeding db."""
#     result = db.session.query(func.max(Trip.trip_id)).one()
#     max_id = int(result[0])
#     # max_id = int(0)

#     query = "SELECT setval('trips_trip_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # load_users()
    # load_trips()
    # load_usertrips()
    # set_val_trip_id()
    # set_val_user_id()
