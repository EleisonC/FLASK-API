import unittest
import os
import json
from app import create_app, db


class RecipeTestCase(unittest.TestCase):
    """ this class contains recipe testcases """

    def setUp(self):
        """ define test variables and initialize the app"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.recipes = {
            "recipe_name": "fries",
            "instructions": "use very good oil"
        }
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

    def test_recipe_creation(self):
        """ Test API can create a recipe (POST request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        category = self.client.post('/category_creation/',
                                    headers=dict(
                                        Authorization="Bearer " + access_token
                                        ),
                                    data=self.categorylist)
        category_id = json.loads(category.data.decode(
            'utf-8').replace("'", "\""))

        res = self.client.post('/create_recipe/{}'.format(category_id['id']),
                               headers=dict(
                                   Authorization="Bearer " + access_token),
                               data=self.recipes)
        self.assertEqual(res.status_code, 201)
        self.assertIn("fries", str(res.data))

    def test_view_recipe(self):
        """ Test API can view all recipes(GET request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        res = self.client.post('/create_recipe/',
                               headers=dict(
                                   Authorization="Bearer " + access_token),
                               data=self.recipes)
        self.assertEqual(res.status_code, 201)
        res = self.client.get('/view_all_recipes/',
                              headers=dict(
                                  Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn("fries", str(res.data))

    def test_view_specific_recipe(self):
        """ Test API can view a specific recipe(GET request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client.post('/create_recipe/',
                              headers=dict(
                                  Authorization="Bearer " + access_token),
                              data=self.recipes)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client.get(
            '/recipe_byid/{}'.format(result_in_json['id']),
            headers=dict(
                Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn("fries", str(result.data))

    def test_recipe_edit(self):
        """ Test API can edit a recipe(PUT requestT)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client.post('/create_recipe/', data={"recipe_name": "posho"})
        self.assertEqual(rv.status_code, 201)
        rv = self.client.put('/recipe_manipulation/1',
                             headers=dict(
                                 Authorization="Bearer " + access_token),
                             data={"recipe_name": "rice"})
        self.assertEqual(rv.status_code, 200)
        results = self.client.get('/recipe_byid/1',
                                  headers=dict(
                                      Authorization="Bearer " + access_token))
        self.assertIn("rice", str(results.data))

    def test_recipe_delete(self):
        """ Test API can delete a recipe(DELETE request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        rv = self.client.post('/create_recipe/',
                              headers=dict(
                                  Authorization="Bearer " + access_token),
                              data={"recipe_name": "beans"})
        self.assertEqual(rv.status_code, 201)
        rv = self.client.delete('/recipe_manipulation/1',
                                headers=dict(
                                    Authorization="Bearer " + access_token))
        self.assertEqual(rv.status_code, 200)
        rv = self.client.get('/recipe_byid/1',
                             headers=dict(
                                 Authorization="Bearer " + access_token))
        self.assertEqual(rv.status_code, 404)

    def tearDown(self):
        """teardown all initalized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == " __main__":
    unittest.main()
