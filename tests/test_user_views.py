import unittest
import os
import json
from app import create_app, db


class UserTestCase(unittest.TestCase):
    """testcases for the authentication Blueprint"""

    def setUp(self):
        """Define test variables and initialize app. """
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.user_data = {
            'email': 'chris@gog.com',
            'username': 'chris',
            'password': 'Chris12'
        }

        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_data_validation(self):
        """ test validity of user data."""
        userdata = {
            "email": "james@gog.com",
            "username": "james",
            "password": "chris"
        }
        res = self.client.post('/auth/register', data=userdata)
        # to get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success
        self.assertEqual(result["message"],
                         'please provide a strong valid password above six characters')
        

    def test_registration(self):
        """test user registration works"""
        res = self.client.post('/auth/register', data=self.user_data)
        # to get the results returned in json format
        result = json.loads(res.data.decode())
        # assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'],
                         'You registered successfully. Please log in.')
        self.assertEqual(res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice"""
        res = self.client.post('/auth/register', data=self.user_data)
        # self.assertEqual(res.status_code, 201)
        second_res = self.client.post('/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 400)
        # get the results returned in json format
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], 'User already exists. Please choose another username'
        )

    def test_user_login(self):
        """Test registered user can login"""
        res = self.client.post('/auth/register', data=self.user_data)
        login_res = self.client.post('/auth/login', data=self.user_data)
        # get results in json format
        result = json.loads(login_res.data.decode())
        # test that the response contains succes message
        self.assertEqual(result['message'], 'You logged in successfully')
        # assert that the status code is equal to 200
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_non_registered_user_login(self):
        """Test non registered users cannot login"""
        # define a dictionary to represent an unregistered user
        not_a_user = {
            'username': 'unknown',
            'password': 'not_available'
        }
        # send a POST request to /auth/login with the data above
        res = self.client.post('/auth/login', data=not_a_user)
        # get the result in json
        result = json.loads(res.data.decode())

        # assert that this response must contain an error message
        # and an error statuscode 401(Unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            result['message'], 'Invalid username or password, please try again'
        )

    def test_user_logout(self):
        """ Test a user can logout"""
        register_res = self.client.post('/auth/register', data=self.user_data)
        login_user = self.client.post('/auth/login', data=self.user_data)
        result = json.loads(login_user.data.decode())
        access_token = result['access_token']
        res = self.client.post('/auth/logout', headers=dict(
            Authorization="Bearer " + access_token))
        data = json.loads(res.data.decode())
        self.assertTrue(data['message'] == 'Logged out Successfully')
        self.assertEqual(res.status_code, 200)

    def test_password_reset(self):
        """ test a user can change password"""
        register_res = self.client.post('/auth/register', data=self.user_data)
        login_user = self.client.post('/auth/login', data=self.user_data)
        result = json.loads(login_user.data.decode())
        access_token = result['access_token']
        res = self.client.put('/auth/reset_password', headers=dict(
            Authorization="Bearer " + access_token), data={
                'username': 'chris',
                'password': 'Chris12',
                'new_password': 'James23',
                'confirm_password': 'James23'
            })
        data = json.loads(res.data.decode())
        self.assertTrue(data['message'] == 'Password Succesfully Changed')
        self.assertEqual(res.status_code, 200)
