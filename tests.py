"""This module holds the test classes."""

import unittest
from server import app
from model import connect_to_db, db, example_data


class FlasksTests(unittest.TestCase):
    """Set up the tests."""

    def setUp(self):
        """Stuff to do before every test."""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "ABC"
        self.client = app.test_client()

    def tearDown(self):
        """Stuff to do after each test."""


class RideshareTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""
        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""
        db.session.close()
        db.drop_all()


class FlaskTestsLoggedIn(unittest.TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Stuff to do before every test."""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "ABC"
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        # Connect to test database
        connect_to_db(app, 'postgresql:///testdb')

        # Create tables and add sample data
        db.create_all()
        example_data()


    def test_login(self):
        """Test login page in homepage."""
        result = self.client.post('/login',
                                  data={"email": "jo@bama.com",
                                        "password": "jo@bama.com"},
                                  follow_redirects=True)
        self.assertIn(b"Welcome", result.data)
        self.assertNotIn(b"Register", result.data)

    def test_logout(self):
        """Test that logout route does log user out."""
        result = self.client.get('/logout', follow_redirects=True)

        self.assertIn(b"Register", result.data)

    def test_homepage(self):
        """Test that register and log-in page is only visible if user is not logged in."""
        result = self.client.get('/')
        self.assertIn(b"Welcome", result.data)
        self.assertNotIn(b"Register", result.data)

    def test_edit_profile(self):
        """Test that information can be edited."""
        result = self.client.post('/edit-profile',
                                  data={"fname": "Linda",
                                        "lname": "Lo",
                                        "gender": "Female",
                                        "phone_number": "123",
                                        "profile_picture": "img",
                                        "social_media": "twitter",
                                        "bio": "Happy go lucky person!"},
                                  follow_redirects=True)
        self.assertIn(b"Welcome", result.data)

    def test_join_ride(self):
        """Test that user is able to join ride."""
        result = self.client.post('/join-ride',
                                  data={'trip': '32'},
                                  follow_redirects=True)

        self.assertIn(b"Welcome", result.data)



    def test_add_ride_page(self):
        """Test that add ride page loads if user is logged in."""
        result = self.client.get('/add-ride', follow_redirects=True)

        self.assertIn(b"Add", result.data)

    def test_add_ride(self):
        """Test that user ride gets added."""
        result = self.client.post('/add-ride',
                                  data={"date": "08-13-2018",
                                        "max_passengers": "2",
                                        "time": "3:24 PM",
                                        "newleg": True,
                                        "cost": "15",
                                        "origin": "San Francisco, CA, USA",
                                        "destination": "San Diego, CA, USA"},
                                  follow_redirects=True)

        self.assertIn(b"Welcome", result.data)

    def test_search_rides_page(self):
        """Test that search ride page loads if user is logged in."""
        result = self.client.get('/search-rides', follow_redirects=True)

        self.assertIn(b"Search rides", result.data)

    def test_search_rides_results(self):
        """Test that search ride gives results if it finds matching data."""
        result = self.client.post('/search-rides',
                                  data={"origin": "San Francisco",
                                        "destination": "Los Angeles",
                                        "date": "07/07/2018"},
                                  follow_redirects=True)

        self.assertIn(b"Available rides", result.data)

    def test_search_rides_no_results(self):
        """Test that search ride gives results if no matching data."""
        result = self.client.post('/search-rides',
                                  data={"origin": "San Diego",
                                        "destination": "Los Angeles",
                                        "date": "07/07/2018"},
                                  follow_redirects=True)

        self.assertIn(b"Sorry", result.data)

    def test_search_rides_nearby_results(self):
        """Test that search ride gives results if it finds matching data."""
        result = self.client.post('/search-rides',
                                  data={"origin": "San Francisco",
                                        "destination": "Anaheim",
                                        "date": "07/07/2018"},
                                  follow_redirects=True)

        self.assertIn(b"nearby", result.data)


class FlaskTestsLoggedOut(unittest.TestCase):
    """Flask tests with user logged out."""

    def setUp(self):
        """Stuff to do before every test."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_homepage(self):
        """Test homepage if user is logged out."""
        result = self.client.get('/', follow_redirects=True)
        self.assertIn(b"Register", result.data)

    def test_add_ride(self):
        """Test add ride page when user is not logged in. User should not be able to view page."""
        result = self.client.get('/add-ride', follow_redirects=True)
        self.assertNotIn(b"Add a ride", result.data)
        self.assertIn(b"Register", result.data)

    def test_search_rides(self):
        """Test request ride page when user is not logged in. User should not be able to view page."""
        result = self.client.get('/search-rides', follow_redirects=True)
        self.assertNotIn(b"Starting", result.data)
        self.assertIn(b"Register", result.data)

    def test_registration(self):
        """Test that user can register."""
        result = self.client.post('/register',
                                  data={"email": "nancy@nancy.com",
                                        "password": "nancyspassword"},
                                  follow_redirects=True)
        self.assertIn(b"Registration completed", result.data)

    def test_landing_page(self):
        """Test landing page shows when user is not logged in."""
        result = self.client.get('/', follow_redirects=True)

        self.assertIn(b"Register", result.data)


if __name__ == "__main__":
    unittest.main()
