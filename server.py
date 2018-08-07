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

    return render_template('homepage.html')

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
        session['user_id'] = user_id
        flash('Yay! You are logged in.')

    return redirect('/')

@app.route('/rides')
def display_trips():
    """Display trips/rides available."""

    return render_template('rides.html')

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

    new_trip = Trip(date_of_trip=date_trip_str,
                    max_passengers=max_passengers,
                    origin=trip_origin,
                    destination=trip_destination,
                    willing_to_stop=willing_to_stop,
                    trip_cost=trip_cost,
                    user_id=user_id)


    return redirect('/rides')






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