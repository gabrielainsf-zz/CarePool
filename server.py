"""
This module holds the view functions for Raite.

Some of the functions help the user log in, search for rides, and add a ride.
"""
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask import jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Trip, UserTrip
from helpers import distance_matrix_filter, distance_matrix
from datetime import datetime, date
from twilio.rest import Client
import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Google Place key
# ONE_EXAMPLE format edit
googlePlaceKey = os.environ['GOOGLE_PLACES_KEY']
twilioSID = os.environ['TWILIO_SID']
twilioAuthKey = os.environ['TWILIO_AUTH_KEY']
twilioNum = os.environ['TWILIO_NUM']
myNum = os.environ['MY_NUM']

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Display Homepage."""
    user_id = session.get('user_id')

    user_info = User.query.filter(User.user_id == user_id).one()

    if user_id:
        return render_template('homepage.html', user_info=user_info)
    else:
        return render_template('index.html')


@app.route('/trips.json')
def trips():
    """Return trips where user is a driver or passenger."""
    user_id = session.get('user_id')

    if user_id:
        trips = Trip.query.filter(Trip.user_id == user_id).all()

        trips_dict_list = []
        trips_by_date = {}

        for trip in trips:
            trip_json = trip.to_json()
            trips_dict_list.append(trip_json)

            passengers = (UserTrip.query.filter(UserTrip.trip_id ==
                                                trip_json["tripId"]).all())
            trip_json["passengers"] = ([passenger.to_json()
                                        for passenger in passengers])

        trips_as_passenger = UserTrip.query.filter(UserTrip.user_id ==
                                                   user_id).all()
        trips_pass_dict = [trip.to_json() for trip in trips_as_passenger]

        for trip in trips_pass_dict:
            trips_by_date[trip['dateOfTrip']] = trip

        for trip in trips_dict_list:
            trips_by_date[trip['dateOfTrip']] = trip

        # for trip, trip2 in zip(trips_pass_dict, trips_dict_list):
        #     trips_by_date[trip['dateOfTrip']] = trip
        #     trips_by_date[trip2['dateOfTrip']] = trip2

        return jsonify({'trips': trips_dict_list,
                        'tripsAsPassenger': trips_pass_dict,
                        'tripsByDate': trips_by_date})
    else:
        flash("Oops! You need to log in.")
        return jsonify({'status': 'You"re not logged in'})


@app.route('/user-info.json')
def user_info():
    """Serialized information for front-end."""
    user_id = session.get('user_id')

    if user_id:
        user_info = User.query.filter(User.user_id == user_id).first()
        user_info_json = user_info.to_json()

        return jsonify({'userInfo': user_info_json})
    else:
        flash("Oops! You need to log in.")
        return jsonify({'status': 'You"re not logged in'})


@app.route('/login', methods=["POST"])
def log_user_in():
    """Log the user in."""
    email = request.form['email']
    password = request.form['password']

    user_by_email = User.query.filter(User.email == email).first()

    # If email is not found in db
    if user_by_email is None:
        flash('Oops! You need to register first.')
    # If email is found in db
    elif user_by_email is not None:
        user_id = user_by_email.user_id
        user_password = user_by_email.password

        # Verify password is correct
        if password != user_password:
            flash("Incorrect password.")

        elif email == user_by_email.email and password == user_password:
            session['user_id'] = user_id
            flash('Logged in successfully')

    return redirect('/')


@app.route('/add-ride')
def add_trip():
    """Add ride to the rides table."""
    user_id = session.get('user_id')

    if user_id:
        return render_template('add_ride.html', key=googlePlaceKey)
    else:
        flash("You need to be logged in to do that.")
        return redirect('/')


@app.route('/add-ride', methods=["POST"])
def add_trip_process():
    """Add a trip to the database."""
    trip_date = request.form['date']
    trip_origin = request.form['origin']
    trip_destination = request.form['destination']
    max_passengers = request.form['max_passengers']
    trip_cost = request.form['cost']
    willing_to_stop = request.form['newleg'] in ('True')
    user_id = session.get('user_id')
    distance_meters, display_distance = (distance_matrix.distance_matrix(
                                         trip_origin,
                                         trip_destination))

    new_trip = Trip(date_of_trip=trip_date,
                    max_passengers=max_passengers,
                    origin=trip_origin,
                    destination=trip_destination,
                    willing_to_stop=willing_to_stop,
                    trip_cost=trip_cost,
                    user_id=user_id,
                    distance_meters=distance_meters,
                    display_distance=display_distance,
                    is_active=True)

    db.session.add(new_trip)
    db.session.commit()

    return redirect('/')


@app.route('/search-rides')
def search_rides_form():
    """Display search ride form."""
    user_id = session.get('user_id')

    if user_id:
        return render_template('search_form.html', key=googlePlaceKey)
    else:
        flash("You need to be logged in to do that.")
        return redirect('/')


@app.route('/search-rides', methods=["POST"])
def search_rides():
    """Display search rides results."""
    origin = request.form['origin']
    destination = request.form['destination']
    date_desired = request.form['date']
    date_obj = datetime.strptime(date_desired, "%m/%d/%Y").date()
    today = date.today()

    # Query for origin and destination, if none, then nearby trips
    trips = Trip.query.filter(Trip.origin == origin,
                              Trip.destination == destination,
                              Trip.date_of_trip >= today).all()

    if not trips:
        # Query trips from origin
        trips_by_origin = Trip.query.filter(Trip.origin == origin,
                                            Trip.date_of_trip >= today).all()

        if not trips_by_origin:
            flash(('Sorry, no rides were found.'
                   'Would you like to try another search?'))
            return redirect('/search-rides')

        else:
            possible_destinations = ([trip.destination
                                      for trip in trips_by_origin])
            drop_offs_nearby = (distance_matrix_filter.distance_matrix_filter(
                                destination,
                                possible_destinations,
                                trips_by_origin))

            if not drop_offs_nearby:
                flash(('Sorry, no rides were found.'
                       'Would you like to try another search?'))
                return redirect('/search-rides')
            else:
                return render_template('nearby_search_results.html',
                                       origin=origin,
                                       destination=destination,
                                       date=date,
                                       date_desired=date_desired,
                                       date_obj=date_obj,
                                       drop_offs_nearby=drop_offs_nearby)
    else:
        return render_template('search_results.html',
                               trips=trips,
                               origin=origin,
                               destination=destination,
                               date_desired=date_desired,
                               date=date,
                               date_obj=date_obj)


@app.route('/join-ride', methods=["POST"])
def create_user_trip():
    """Add user to ride in the database."""
    trip_id = request.form['trip']
    user_id = session.get('user_id')

    trip = Trip.query.filter(Trip.trip_id == trip_id).one()

    # Ensure there is still space before adding to current passengers
    if trip.num_passengers < trip.max_passengers:

        trip.num_passengers += 1

        new_user_trip = UserTrip(trip_id=trip_id,
                                 user_id=user_id)

        db.session.add(new_user_trip)
        db.session.commit()

        flash("Ride joined!")
        return redirect('/')
    else:
        flash("Sorry, ride is already full!")
        return redirect('/')


@app.route('/notify', methods=["POST"])
def notify_user():
    """Send text message to passenger/driver with Twilio API."""
    client = Client(twilioSID, twilioAuthKey)
    msg = request.form.get("message")

    client.messages.create(to=myNum, from_=twilioNum, body=msg)

    flash('Message sent!')
    return redirect('/')


@app.route('/logout')
def logout():
    """Log user out."""
    del session['user_id']
    flash('Logged out!')

    return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
