from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Trip, UserTrip



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Display Homepage."""

    user_id = session['user_id']

    upcoming_trips = Trip.query.filter(Trip.user_id == user_id).all()

    return render_template('homepage.html', upcoming_trips=upcoming_trips)

@app.route('/login')
def display_login_form():

    return render_template('login_form.html')

@app.route('/login', methods=["POST"])
def login_process():

    # Form data
    email = request.form['email']
    password = request.form['password']

    # DB data
    user_by_email = User.query.filter(User.email == email).first()
    user_password = user_by_email.password
    user_id = user_by_email.user_id

    # Verify user is registered
    if user_by_email is None:
        flash('Oops! You need to register first.')
    elif email == user_by_email.email and password == user_by_email.password:
        session['user_id'] = user.user_id
        flash('Yay! You are logged in.')

    return redirect('/')

@app.route('/add-ride')
def add_trip():

    return render_template('add_ride.html')

@app.route('/add-ride', methods=["POST"])
def add_trip_process():
    """Adds a trip to the database."""

    trip_date = request.form["date"]
    trip_origin = request.form["origin"]
    trip_destination = request.form["destination"]
    max_passengers = request.form["max_passengers"]
    trip_cost = request.form["cost"]
    willing_to_stop = request.form["newleg"]
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

    return render_template('search_form.html')

@app.route('/search-rides', methods=["POST"])
def search_rides():

    user_id = session.get('user_id')

    # Data from form
    origin = request.form['origin']
    destination = request.form['destination']

    # Data from query
    trips = Trip.query.filter(Trip.origin == origin, Trip.destination == destination).all()
    
    if trips is None:
        flash("Sorry, no rides were found. Would you like to try another search?")
        return redirect('/search-rides')
    else:
        return render_template('search_results.html', trips=trips, origin=origin, destination=destination)

@app.route('/request-ride', methods=["POST"])
def create_user_trip():

    trip_id = request.form['trip']
    user_id = session.get('user_id')

    trip = Trip.query.filter(Trip.trip_id == trip_id).one()

    # Ensure there is still space before adding to current passengers
    if trip.num_passengers < trip.max_passengers:
        
        # Increment number of passengers in ride
        trip.num_passengers += 1

        # Instantiate new UserTrip obj
        new_user_trip = UserTrip(trip_id=trip_id,
                             user_id=user_id)

        db.session.add(new_user_trip)
        db.session.commit()
        flash("Ride requested!")
        return redirect('/')
    else:
        flash("Sorry, ride is already full!")

# @app.route('/update-ride')
# def update_trip():

#     return render_template('edit_ride.html')

# @app.route('/update-ride', methods=["POST"])
# def update_trip_process():

#     return redirect('/')






if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')