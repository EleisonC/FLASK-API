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

    def test_category_creation(self):
        """Test API can create a categorylist (POST request) """
        res = self.client.post('/category_creation/', data=self.categorylist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Lunch', str(res.data))

    def test_api_can_get_all_categories(self):
        """Test API can get a category (Get request)"""
        res = self.client.post('/category_creation/', data=self.categorylist)
        self.assertEqual(res.status_code, 201)
        res = self.client.get('/category_view_all/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Lunch', str(res.data))

    def test_api_can_get_category_by_id(self):
        """Test API can get a single category by using """
        rv = self.client.post('/category_creation/', data=self.categorylist)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'","\""))
        result = self.client.get(
            '/category_manipulation/{}'.format(result_in_json['id'])
        )
        self.assertEqual(result.status_code, 200)
        self.assertIn('Lunch', str(result.data))

    def test_category_can_be_edited(self):
        """Test API can edit an existing category. (Put request)"""
        rv = self.client.post(
            '/category_creation/',
            data={'category_name': 'Breakfast'}
        )
        self.assertEqual(rv.status_code, 201)
        rv = self.client.put(
            '/category_manipulation/1',  
            data={'category_name': 'Soups'}
        )
        self.assertEqual(rv.status_code, 200)
        results = self.client.get('/category_manipulation/1')
        self.assertIn('Soups', str(results.data))

    def test_categorylist_deletion(self):
        """Test API can delete an exsisting category. (DELETE request)."""
        rv = self.client.post(
            '/category_creation/',
            data={'category_name': 'Dinner'}
        )
        self.assertEqual(rv.status_code, 201)
        res = self.client.delete('/category_manipulation/1')
        self.assertEqual(res.status_code, 200)
        result = self.client.get('/category_manipulation/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initalized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == " __main__":
    unittest.main()
