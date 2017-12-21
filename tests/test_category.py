import unittest
import os
import json
from app import create_app, db


class CategorylistTestCase(unittest.TestCase):
    """This class represents the categorylist test case """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.categorylist = {'category_name': 'Lunch'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def register_user(self, username="Chris", password="Chris32"):
        """This helper method helps register a test user."""
        user_data = {
            'username': username,
            'password': password
        }
        return self.client.post('/auth/register', data=user_data)

    def login_user(self, username="Chris", password="Chris32"):
        """ this helper method helps login a registered user"""
        user_data = {
            'username': username,
            'password': password
        }
        return self.client.post('/auth/login', data=user_data)

    def test_category_creation(self):
        """Test API can create a categorylist (POST request) """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client.post('/category_creation/',
                               headers=dict(
                                   Authorization="Bearer " + access_token),
                               data=self.categorylist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Lunch', str(res.data))

    def test_api_can_get_all_categories(self):
        """Test API can get a category (Get request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client.post('/category_creation/',
                               headers=dict(
                                   Authorization="Bearer " + access_token),
                               data=self.categorylist)
        self.assertEqual(res.status_code, 201)
        res = self.client.get('/category_view_all/',
                              headers=dict(
                                  Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn('Lunch', str(res.data))

    def test_api_can_get_category_by_id(self):
        """Test API can get a single category by using """
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client.post('/category_creation/',
                              headers=dict(
                                  Authorization="Bearer " + access_token),
                              data=self.categorylist)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client.get(
            '/category_manipulation/{}'.format(result_in_json['category_id']),
            headers=dict(Authorization="Bearer " + access_token)
        )
        self.assertEqual(result.status_code, 200)
        self.assertIn('Lunch', str(result.data))

    def test_pagination(self):
        """ test pagination"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        rv = self.client.post('/category_creation/',
                              headers=dict(
                                  Authorization="Bearer " + access_token),
                              data=self.categorylist)
        result = self.client.get(
            '/category_view_all/?page=1&per_page=5',
            headers=dict(Authorization="Bearer " + access_token)
        )
        self.assertEqual(result.status_code, 200)
        self.assertIn('Lunch', str(result.data))

    def test_get_category_by_query(self):
        """ Test API can get categories by query"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client.post('/category_creation/',
                              headers=dict(
                                  Authorization="Bearer " + access_token),
                              data=self.categorylist)
        result = self.client.get(
            '/category_view_all/?q=Lunch',
            headers=dict(Authorization="Bearer " + access_token)
        )
        self.assertEqual(result.status_code, 200)
        self.assertIn('Lunch', str(result.data))

    def test_category_can_be_edited(self):
        """Test API can edit an existing category. (Put request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client.post(
            '/category_creation/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'category_name': 'Breakfast'}
        )
        self.assertEqual(rv.status_code, 201)
        rv = self.client.put(
            '/category_manipulation/1',
            headers=dict(Authorization="Bearer " + access_token),
            data={'category_name': 'Soups'}
        )
        self.assertEqual(rv.status_code, 200)
        results = self.client.get('/category_manipulation/1',
                                  headers=dict(
                                      Authorization="Bearer " + access_token))
        self.assertIn('Soups', str(results.data))

    def test_categorylist_deletion(self):
        """Test API can delete an exsisting category. (DELETE request)."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client.post(
            '/category_creation/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'category_name': 'Dinner'}
        )
        self.assertEqual(rv.status_code, 201)
        res = self.client.delete('/category_manipulation/1',
                                 headers=dict(
                                     Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        result = self.client.get('/category_manipulation/1',
                                 headers=dict(
                                     Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initalized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == " __main__":
    unittest.main()
