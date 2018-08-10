from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Trip, UserTrip
import requests
import os
# from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
# import flask_login



app = Flask(__name__)
# login = LoginManager(app)


# Image uploads
# photos = UploadSet('photos', IMAGES)
# app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
# configure_uploads(app, photos)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Display Homepage."""

    user_id = session.get('user_id')

    if user_id:
        upcoming_trips = Trip.query.filter(Trip.user_id == user_id).all()
        return render_template('homepage.html', upcoming_trips=upcoming_trips)
    else:
        flash("Oops! You need to log in.")
        return render_template('login_form.html')

############# Flask-Login attempt ##########

# @login.user_loader
# def load_user():
    
#     return User.query.get(user_id)


# @app.route('/login', methods=["GET, POST"])
# def login():
#     form = LoginForm()

#     if form.validate_on_submit():
#         user = User.query.get(form.email.data)
#         if user:
#             if bcrypt.check_password_hash(user.password, form.password.data):
#                 user.authenticated = True
#                 db.session.add(user)
#                 db.session.commit()
#                 login_user(user, remember=True)
#                 return redirect('/')

#     return render_template("login_form.html", form=form)

#############################

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

    return redirect('/')

@app.route('/add-ride')
def add_trip():

    user_id = session.get('user_id')

    if user_id:
        return render_template('add_ride.html')
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
    willing_to_stop = request.form['newleg']
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

#######
# @app.route('/autocomplete')
# def autocomplete_search():

#     return render_template('googleplaces.html')
######

@app.route('/search-rides')
def search_rides_form():

    user_id = session.get('user_id')

    key = os.environ['GOOGLE_PLACES_KEY']

    # If user is in session
    if user_id:
        return render_template('search_form.html', key=key)
    else:
        flash("You need to be logged in to do that.")
        return redirect('/login')


@app.route('/search-rides', methods=["POST"])
def search_rides():

    # Data from form
    origin = request.form['origin']
    destination = request.form['destination']

    print(origin)
    print(type(origin))

    # Data from query
    trips = Trip.query.filter(Trip.origin == origin,
                              Trip.destination == destination).all()
    print("\n\nTRIPS")
    print(trips)
    if not trips:
        flash("Sorry, no rides were found. Would you like to try another search?")
        return redirect('/search-rides')
    else:
        return render_template('search_results.html',
                                trips=trips,
                                origin=origin,
                                destination=destination)



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

# @app.route('/update-ride', methods=["POST"])
# def update_trip():

#     trip_id = request.form['trip']

#     return render_template('update_ride.html', trip_id=trip_id)

# @app.route('/update-ride-submit', methods=["POST"])
# def update_trip_process():

#     trip_id = request.form['trip']

#     # Data from form
#     trip_date = request.form.get('date', None)
#     trip_origin = request.form.get('origin', None)
#     trip_destination = request.form.get('destination', None)
#     max_passengers = request.form.get('max_passengers', None)
#     trip_cost = request.form.get('cost', None)
#     willing_to_stop = request.form.get('newleg', None)

#     # Data from query
#     trip = Trip.query.filter(Trip.trip_id == trip_id)

#     # Update row
#     # Write in conditionals, check if there is data returned or Null value to update
#     if trip_date is not None:
#         trip.trip_date = trip_date

#         flash("Ride updated!")
    
#     return redirect('/')



@app.route('/logout')
def logout():
    """Log user out."""

    del session['user_id']
    flash('Logged out!')

    return redirect('/')
    # Later change to landing page


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