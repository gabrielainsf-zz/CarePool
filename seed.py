"""Utility file to seed user and trip information."""

from sqlalchemy import func
from model import connect_to_db, db
from model import User, Trip
from model import UserTrip
from server import app
from datetime import datetime
from random import choice

def load_users():
    """Load users from MOCK_USER_DATA into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    for row in open("seed_data/MOCK_USER_DATA.csv"):
        row = row.rstrip()
        row_list = row.split(",")
        # print(row_list)

        user_id = row_list[0]
        # print(user_id)
        first_name = row_list[1] 
        last_name = row_list[2]
        email = row_list[3]
        gender = row_list[4]
        password = row_list[5]
        profile_photo = row_list[6]
        user_bio = row_list[7]
        social_media = row_list[8]
        # print(social_media)

        user = User(user_id=user_id,
                    fname=first_name,
                    lname=last_name,
                    email=email,
                    password=password,
                    user_gender=gender,
                    user_bio=user_bio,
                    user_profile_img=profile_photo,
                    user_social_media=social_media)


        db.session.add(user)
    db.session.commit()

def load_trips():
    """Load trips from MOCK_TRIP_DATA into database."""

    print("Trips")

    Trip.query.delete()

    for row in open("seed_data/MOCK_TRIP_DATA.csv"):
        row = row.rstrip()
        row_list = row.split(",")

        trip_id = row_list[0]
        origin = row_list[1]
        destination = row_list[2]
        date_trip_str = row_list[3]
        # date_trip = datetime.strptime(date_trip_str, "%d-%b-%Y")
        willing_to_stop = row_list[4]
        max_passengers = row_list[5]
        num_passengers = 2
        trip_cost = 15

        user_id = row_list[6]
        if User.query.get(user_id):
            trip = Trip(trip_id=trip_id,
                        date_of_trip=date_trip_str,
                        max_passengers=max_passengers,
                        num_passengers = num_passengers,
                        origin=origin,
                        destination=destination,
                        willing_to_stop=willing_to_stop,
                        trip_cost=trip_cost,
                        user_id=user_id)
        else:
            random_users = User.query.all()
            user_id = choice(random_user)
            trip = Trip(trip_id=trip_id,
                        date_of_trip=date_trip_str,
                        max_passengers=max_passengers,
                        num_passengers = num_passengers,
                        origin=origin,
                        destination=destination,
                        trip_cost=trip_cost,
                        user_id=user_id)




        db.session.add(trip)

    db.session.commit()


def load_usertrips():
    """Load user trips."""

    print("User Trips")

    UserTrip.query.delete()

    user_trip = UserTrip(trip_id=12,
                         user_id=25)

    db.session.add(user_trip)
    db.session.commit()

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_trip_id():
    """Set value for the next trip after seeding db"""

    result = db.session.query(func.max(Trip.trip_id)).one()
    max_id = int(result[0])

    query = "SELECT setval('trips_trip_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    load_users()
    load_trips()
    load_usertrips()
    set_val_trip_id()
    set_val_user_id()