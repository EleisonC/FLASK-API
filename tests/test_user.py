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
            'username': 'chris',
            'password': '1234'
        }

        with self.app.app_context():
            #create all tables
            db.session.close()
            db.drop_all()
            db.create_all()
        

    def test_registration(self):
        """test user registration works"""
        res = self.client.post('/auth/register', data=self.user_data)
        # to get the results returned in json format
        result = json.loads(res.data.decode())
        #assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'], 'You registered successfully. Please log in.')
        self.assertEqual(res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice"""
        res = self.client.post('/auth/register', data=self.user_data)
        
        # self.assertEqual(res.status_code, 201)
        second_res = self.client.post('/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 202)
        #get the results returned in json format
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], 'User already exists. Please login'
        )