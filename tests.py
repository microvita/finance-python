import unittest
from application import create_app, db
from application.models import User, Note

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use an in-memory SQLite database for testing
        self.client = self.app.test_client()  # Create a test client to simulate requests
        with self.app.app_context():
            db.create_all()
            # Create some sample data for testing
            user = User(email='test@example.com', full_name='Test User', password='test_password')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register(self):
        response = self.client.post('/register', data=dict(full_name='New User', email='new_user@example.com', password='new_password', confirm_password='new_password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account created! You are now logged in.', response.data)

    def test_login(self):
        response = self.client.post('/login', data=dict(email='new_user@example.com', password='new_password'))
        self.assertEqual(response.status_code, 200)

    def test_home_post_method_with_valid_note(self):
        # Log in the user
        self.client.post('/login', data=dict(email='test@example.com', password='test_password'), follow_redirects=True)

        # Simulate a POST request to the home page with a valid note
        response = self.client.post('/', data=dict(note='Test Note'), follow_redirects=True)



if __name__ == '__main__':
    unittest.main()
