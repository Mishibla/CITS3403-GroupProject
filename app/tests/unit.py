from unittest import TestCase

from flask import url_for

from app import create_app, db
from app.config import TestConfig
from app.controllers import AccountCreationError, create_user, get_user,create_account
from app.models import User
from app.forms import RegisterForm

from werkzeug.datastructures import MultiDict


class BasicUnitTests(TestCase):

    def setUp(self):
        testApp = create_app(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        self.client = testApp.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        # Create a new user instance using the controller function
        user = create_user('Mishibla', 'chris', 'cat', 'random@gmail.com')
        # Retrieve the user and check the password
        retrieved_user = get_user('Mishibla')
        self.assertTrue(retrieved_user.check_password('cat'))
        self.assertFalse(retrieved_user.check_password('dog'))


    def test_register_account_duplicate_username(self):
        with self.assertRaisesRegex(AccountCreationError, 'testuser has already been created, please enter a unique username'):
            with self.app_context:
                form_data = MultiDict({
                    'username': 'testuser',
                    'display_name': 'Test User',
                    'password': 'testpassword',
                    'email': 'test@example.com',
                    'phone': '1234567890'
                })
                form = RegisterForm(form_data)
                create_account(form)

                duplicate_form_data = MultiDict({
                    'username': 'testuser',
                    'display_name': 'Another User',
                    'password': 'anotherpassword',
                    'email': 'another@example.com',
                    'phone': '0987654321'
                })
                duplicate_form = RegisterForm(duplicate_form_data)
                create_account(duplicate_form)
'''
    def test_register_account_long_username(self):
        with self.client:
            response = self.client.post(url_for('main.register_account'), data=dict(
                username='a'*30,  # Too long
                display_name='Test User',
                password='testpassword',
                email='test@example.com',
                phone='1234567890',
                submit=True
            ), follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Username is too long', response.data)

    def test_register_account_long_display_name(self):
        with self.client:
            response = self.client.post(url_for('main.register_account'), data=dict(
                username='testuser',
                display_name='a'*30,  # Too long
                password='testpassword',
                email='test@example.com',
                phone='1234567890',
                submit=True
            ), follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Display name is too long', response.data)

    def test_register_account_long_password(self):
        with self.client:
            response = self.client.post(url_for('main.register_account'), data=dict(
                username='testuser',
                display_name='Test User',
                password='a'*20,  # Too long
                email='test@example.com',
                phone='1234567890',
                submit=True
            ), follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Password is too long', response.data)
    def test_register_account_success(self):
        with self.client:
            response = self.client.post(url_for('main.register_account'), data=dict(
                username='testuser',
                display_name='Test User',
                password='testpassword',
                email='test@example.com',
                phone='1234567890',
                submit=True
            ), follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.name, 'Test User')
            self.assertTrue(user.check_password('testpassword'))
            self.assertEqual(user.email, 'test@example.com')
            self.assertEqual(user.phone, '1234567890')

            '''