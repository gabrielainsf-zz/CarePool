"""This module holds the test classes."""

import unittest
from server import app
from model import connect_to_db, db, example_data

class FlasksTests(unittest.TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "ABC"
        self.client = app.test_client()

    def tearDown(self):
        """Stuff to do after each test."""

    # def test_add_ride(self):
    #     """Test that user is logged in order to access add ride page."""




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
        """Test login page in homepage"""

        result = self.client.post('/login',
                                  data={"email": "jo@bama.com",
                                        "password": "jo@bama.com"},
                                  follow_redirects=True)
        self.assertIn(b"Welcome", result.data)
        self.assertNotIn(b"Register", result.data)

    def test_homepage(self):
        """Test that register and log-in page is only visible if user is not logged in."""

        result = self.client.get('/')
        self.assertIn(b"Welcome", result.data)
        self.assertNotIn(b"Register", result.data)


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
        """Test add ride page when user is not logged in. User should not be able
        to view page. """

        result = self.client.get('/add-ride', follow_redirects=True)
        self.assertNotIn(b"Add a ride", result.data)
        self.assertIn(b"Register", result.data)

    def test_search_rides(self):
        """Test request ride page when user is not logged in. User should not be
        able to view page."""

        result = self.client.get('/search-rides', follow_redirects=True)
        self.assertNotIn(b"Starting", result.data)
        self.assertIn(b"Register", result.data)

if __name__ == "__main__":
    unittest.main()