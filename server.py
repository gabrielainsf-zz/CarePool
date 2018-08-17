from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, json, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Trip, UserTrip
from datetime import datetime, date
from googlemaps import convert
from googlemaps.convert import as_list
from twilio.rest import Client
import requests
import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Google Place key
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
    today = date.today()

    if user_id:
        trips = Trip.query.filter(Trip.user_id == user_id).all()
        trips_as_passenger = UserTrip.query.filter(UserTrip.user_id == user_id).all()

        return render_template('homepage.html',
                                trips=trips,
                                today=today,
                                trips_as_passenger=trips_as_passenger,
                                user_id=user_id)
    else:
        flash("Oops! You need to log in.")
        return render_template('login_form.html')

@app.route('/2')
def index2():

    user_id = session.get('user_id')

    if user_id:
        return render_template('homepage2.html')
    else:
        flash("Oops! You need to log in.")
        return jsonify({'status': 'You"re not logged in'})

@app.route('/trips.json')
def trips():
    """Return trips where user is a driver or passenger."""

    user_id = session.get('user_id')

    if user_id:
        trips = Trip.query.filter(Trip.user_id == user_id).all()
        trips_dict = [trip.to_json() for trip in trips]

        trips_as_passenger = UserTrip.query.filter(UserTrip.user_id == user_id).all()
        trips_pass_dict = [trip.to_json() for trip in trips_as_passenger] 
               
        return jsonify({'trips': trips_dict,
                        'trips_as_pass': trips_pass_dict})
    else:
        flash("Oops! You need to log in.")
        return jsonify({'status': 'You"re not logged in'})


@app.route('/login')
def display_login_form():

    return render_template('login_form.html')


@app.route('/login', methods=["POST"])
def login_process():

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
            flash('Yay! You are logged in.')

    return redirect('/2')

@app.route('/add-ride')
def add_trip():
    """Adds ride to the rides table."""

    user_id = session.get('user_id')

    if user_id:
        return render_template('add_ride.html', key=googlePlaceKey)
    else:
        flash("You need to be logged in to do that.")
        return redirect('/login')

@app.route('/add-ride', methods=["POST"])
def add_trip_process():
    """Adds a trip to the database."""

    trip_date = request.form['date']
    trip_origin = request.form['origin']
    trip_destination = request.form['destination']
    max_passengers = request.form['max_passengers']
    trip_cost = request.form['cost']
    willing_to_stop = request.form['newleg'] in ('True') 
    user_id = session['user_id']

    new_trip = Trip(date_of_trip=trip_date,
                    max_passengers=max_passengers,
                    origin=trip_origin,
                    destination=trip_destination,
                    willing_to_stop=willing_to_stop,
                    trip_cost=trip_cost,
                    user_id=user_id)

    db.session.add(new_trip)
    db.session.commit()

    return redirect('/')


@app.route('/search-rides')
def search_rides_form():

    user_id = session.get('user_id')

    # If user is in session
    if user_id:
        return render_template('search_form.html', key=googlePlaceKey)
    else:
        flash("You need to be logged in to do that.")
        return redirect('/login')


@app.route('/search-rides', methods=["POST"])
def search_rides():

    # Data from form
    origin = request.form['origin']
    destination = request.form['destination']
    date = request.form['date']
    date_obj = datetime.strptime(date, "%m/%d/%Y").date()
    # print(date)
    # print(date_obj)


    # Data from query - list of trips from origin

    # Query for origin and destination, if none, then nearby trips
    trips = Trip.query.filter(Trip.origin == origin,
                              Trip.destination == destination).all()

    if not trips:
        # Query trips from origin
        trips = Trip.query.filter(Trip.origin == origin).all()

        if not trips:
            flash("Sorry, no rides were found. Would you like to try another search?")
            return redirect('/search-rides')

        else:
            drop_offs = []
            for trip in trips:
                drop_offs.append(trip.destination)

            # Google Distance Matrix API set up
            base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
            origins = destination
            destinations = drop_offs
            payload = {
                "origins": convert.location_list(origins),
                "destinations": convert.location_list(destinations)
            }

            r = requests.get(base_url, params = payload)

            # Will be a list of tuples with possible drop-off and distance from desired
            # destination
            drop_off_distances = {};

            # Check the HTTP status code returned by the server. Only process the response, 
            # if the status code is 200 (OK in HTTP terms).
            if r.status_code != 200:
                print('HTTP status code {} received, program terminated.'.format(r.status_code))
            else:
                x = json.loads(r.text)
                for isrc, src in enumerate(x['origin_addresses']):
                    for idst, dst in enumerate(x['destination_addresses']):
                        row = x['rows'][isrc]
                        cell = row['elements'][idst]
                        if cell['status'] == 'OK':
                            # Dictionary of drop off distances to key in by city
                            drop_off_distances[dst] = cell['distance']['text']
                            # print('{} to {}: {}.'.format(src, dst, cell['distance']['text']))
                        else:
                            print('{} to {}: status = {}'.format(src, dst, cell['status']))

            def convert_to_int_float(value):
                try:
                    return float(value)
                except ValueError:
                    # return float(value)
                    return int(value.replace(",", ""))

            for drop_off in drop_off_distances:
                # Convert str to float
                kilometers = drop_off_distances[drop_off]
                kilometers = kilometers.split(' ')
                kilometers.pop(1)
                kms = ' '.join(kilometers)
                drop_off_distances[drop_off] = convert_to_int_float(kms)

            # Remove drop-offs with greater distance than 40kms
            # Loop through listified of dict to avoid RunTime error
            for drop_off, distance in list(drop_off_distances.items()):
                if distance > 45:
                    drop_off_distances.pop(drop_off)
            
            # Dictionary that will store trip id, distance
            drop_offs_nearby = {}
            # Consider if there are multiple trips, what happens then to trip_ids since
            # they will be reassigned
            for drop_off in drop_off_distances:     
                for trip in trips:
                    if trip.destination == drop_off:
                        drop_offs_nearby[drop_off] = {'distance': drop_off_distances[drop_off],
                                                      'trip_info': trip,
                                                      'trip_id': trip.trip_id}
            # Example outpout: {'Los Angeles, CA, USA': {'trip_id': 103, 'distance': 1.0},
            #                   'Anaheim, CA, USA': {'trip_id': 104, 'distance': 42.2}}

            return render_template('nearby_search_results.html',
                                    trips=trips,
                                    origin=origin,
                                    destination=destination,
                                    date=date,
                                    date_obj=date_obj,
                                    drop_offs_nearby=drop_offs_nearby)
    else:
        return render_template('search_results.html',
                                trips=trips,
                                origin=origin,
                                destination=destination,
                                date=date,
                                date_obj=date_obj)


@app.route('/join-ride', methods=["POST"])
def create_user_trip():

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

# @app.route('/notify', methods=["GET"])
    
#     return render_template('send_notification.html')

@app.route('/notify', methods=["POST"])
def notify_user():

    client = Client(twilioSID, twilioAuthKey)

    msg = request.form.get("msg")

    message = client.messages.create(
        to=myNum,
        from_=twilioNum,
        body=msg)


@app.route('/logout')
def logout():
    """Log user out."""

    del session['user_id']
    flash('Logged out!')

    return redirect('/login')
    # Later change to landing page


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