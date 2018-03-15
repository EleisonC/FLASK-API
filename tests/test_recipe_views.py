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

    def register_user(self, email='chris@gog.com', username="Chris", password="Chris32"):
        """This helper method helps register a test user."""
        user_data = {
            'email': email,
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

        res = self.client.post('/create_recipe/{}'.format(
            category_id['category_id']),
            headers=dict(
            Authorization="Bearer " + access_token),
            data=self.recipes)
        self.assertEqual(res.status_code, 201)
        self.assertIn("Fries", str(res.data))

    def test_view_recipe(self):
        """ Test API can view all recipes(GET request)"""
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

        res = self.client.post('/create_recipe/{}'.format(
            category_id['category_id']),
            headers=dict(
            Authorization="Bearer " + access_token),
            data=self.recipes)
        self.assertEqual(res.status_code, 201)
        res = self.client.get('/view_recipes/{}/'.format(
            category_id['category_id']),
            headers=dict(
            Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn("Fries", str(res.data))

    def test_view_by_query(self):
        """ Test API can view all recipes(GET request)"""
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

        res = self.client.post('/create_recipe/{}'.format(
            category_id['category_id']),
                            headers=dict(
                                Authorization="Bearer " + access_token),
                                data=self.recipes)
        res = self.client.get('/view_recipes/{}/?q=fries'.format(
            category_id['category_id']),
                              headers=dict(
                                  Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn("Fries", str(res.data))
    def test_pagination_recipes(self):
        """ test pagination in the get method"""
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

        res = self.client.post('/create_recipe/{}'.format(
            category_id['category_id']),
                            headers=dict(
                                Authorization="Bearer " + access_token),
                                data=self.recipes)
        res = self.client.get('/view_recipes/{}/?page=1&per_page=5'.format(
            category_id['category_id']),
                              headers=dict(
                                  Authorization="Bearer " + access_token))
        self.assertEqual(res.status_code, 200)
        self.assertIn("Fries", str(res.data))

    def test_view_specific_recipe(self):
        """ Test API can view a specific recipe(GET request)"""
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

        rv = self.client.post('/create_recipe/{}'.format(
            category_id['category_id']),
            headers=dict(
            Authorization="Bearer " + access_token),
            data=self.recipes)

        self.assertEqual(rv.status_code, 201)

        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client.get(
            '/recipe_byid/{}/{}'.format(category_id['category_id'],
                                        result_in_json['recipe_id']
                                        ),
            headers=dict(
                Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn("Fries", str(result.data))

    def test_recipe_edit(self):
        """ Test API can edit a recipe(PUT requestT)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        category = self.client.post('/category_creation/',
                                    headers=dict(
                                        Authorization="Bearer " + access_token
                                    ),
                                    data={"category_name": "breakfast"})
        category_id = json.loads(category.data.decode(
            'utf-8').replace("'", "\""))

        rv_1 = self.client.post('/create_recipe/{}'.format(
            category_id['category_id']),
                                headers=dict(
                                Authorization="Bearer " + access_token),
                                data={"recipe_name": "posho"})
        self.assertEqual(rv_1.status_code, 201)
        rv_2 = self.client.put('/recipe_edit/{}/1'.format(
            category_id['category_id']),
            headers=dict(
            Authorization="Bearer " + access_token),
            data={"recipe_name": "rice",
                  'instructions': 'Do this and that'})
        self.assertEqual(rv_2.status_code, 200)
        results = self.client.get('/recipe_byid/{}/1'.format(
            category_id['category_id']),
            headers=dict(
            Authorization="Bearer " + access_token))
        self.assertIn("Rice", str(results.data))
    
    def test_recipe_cannot_be_registered_twice(self):
        """ Test api can't allow a category to be registered twice."""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        category = self.client.post('/category_creation/',
                                    headers=dict(
                                        Authorization="Bearer " + access_token
                                    ),
                                    data={"category_name": "breakfast"})
        category_id = json.loads(category.data.decode(
            'utf-8').replace("'", "\""))
        res_1 = self.client.post('/create_recipe/{}'.format(
            category_id['category_id']),
            headers=dict(
            Authorization="Bearer " + access_token),
            data={"recipe_name": "beans"})
        res_2 = self.client.post('/create_recipe/{}'.format(
            category_id['category_id']),
            headers=dict(
            Authorization="Bearer " + access_token),
            data={"recipe_name": "beans"})
        result = json.loads(res_2.data.decode())
        self.assertEqual(result['message'],
                         'The Recipe Already Exists. Try another')

    def test_data_validity(self):
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']
        category = self.client.post('/category_creation/',
                                    headers=dict(
                                        Authorization="Bearer " + access_token
                                    ),
                                    data={"category_name": "breakfast"})
        category_id = json.loads(category.data.decode(
            'utf-8').replace("'", "\""))
        res_1 = self.client.post('/create_recipe/{}'.format(
            category_id['category_id']),
            headers=dict(
            Authorization="Bearer " + access_token),
            data={"recipe_name": "   "})
        result = json.loads(res_1.data.decode())
        self.assertEqual(result['message'],
                         'Enter valid data')

    def test_recipe_delete(self):
        """ Test API can delete a recipe(DELETE request)"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        category = self.client.post('/category_creation/',
                                    headers=dict(
                                        Authorization="Bearer " + access_token
                                    ),
                                    data={"category_name": "breakfast"})
        category_id = json.loads(category.data.decode(
            'utf-8').replace("'", "\""))

        rv = self.client.post('/create_recipe/{}'.format(
            category_id['category_id']),
            headers=dict(
            Authorization="Bearer " + access_token),
            data={"recipe_name": "beans"})
        self.assertEqual(rv.status_code, 201)
        rv = self.client.delete('/recipe_delete/{}/1'.format(
            category_id['category_id']),
            headers=dict(
            Authorization="Bearer " + access_token))
        self.assertEqual(rv.status_code, 200)
        rv = self.client.get('/recipe_byid/{}/1'.format(
            category_id['category_id']),
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
