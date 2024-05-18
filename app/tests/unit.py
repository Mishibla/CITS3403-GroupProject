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
                _data =['testuser','Test User', 'testpassword', 'test@example.com', '1234567890']
                create_account(_data)
                dupli=['testuser','Another User', '123testpassword', '123test@example.com', '002100545']
                create_account(dupli)

    def test_register_account_long_username(self):
        with self.assertRaisesRegex(AccountCreationError, 'Username is too long: max 29 characters, current length 30 characters'):
            with self.app_context:
                _data=['a'*30, 'Test User','testpassword', 'test@example.com', '1234567890']
                create_account(_data)

    def test_register_account_long_display_name(self):
        with self.assertRaisesRegex(AccountCreationError, 'Display name is too long: max 29 characters, current length 30 characters'):
            with self.app_context:
                _data=['a', 'a'*30,'testpassword', 'test@example.com', '1234567890']
                create_account(_data)

    def test_register_account_long_password(self):
        with self.assertRaisesRegex(AccountCreationError, 'Password is too long: max 19 characters, current length 20 characters'):
            with self.app_context:
                _data=['a', 'a','a'*20, 'test@example.com', '1234567890']
                create_account(_data)
            
    def test_register_account_success(self):
        with self.client:
            _data=['testuser', 'Test User','testpassword', 'test@example.com', '1234567890']
            create_account(_data)
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.name, 'Test User')
            self.assertTrue(user.check_password('testpassword'))
            self.assertEqual(user.email, 'test@example.com')
            self.assertEqual(user.phone, '1234567890')

        