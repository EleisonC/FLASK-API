[![Build Status](https://travis-ci.org/EleisonC/FLASK-API.svg?branch=develop)](https://travis-ci.org/EleisonC/FLASK-API)
[![Coverage Status](https://coveralls.io/repos/github/EleisonC/FLASK-API/badge.svg?branch=develop)](https://coveralls.io/github/EleisonC/FLASK-API?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/9598704ef35fafd8d6eb/maintainability)](https://codeclimate.com/github/EleisonC/FLASK-API/maintainability)
## Yummy-Recipes-API
This is a Flask API of the Yummy-Recipes that handles:
1. User authentication
2. Creating, reading, updating and deleting of recipe categories
3. Creating, reading, updating and deleting of recipes

#### To test the application and get it running, do the following:
1. Create the virtual environment and activate
 ```
 $ mkvirtualenv my_project
 $ workon my_project
 ```
 
2. Install the requirements file for all the dependencies of the application
```
$ pip install -r requirements.txt
```

3. Create the database and run migrations
```
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

4. Run the application
```
$ python run.py 
```
5. Run the application tests
```
$ python manage.py test
```

#### Features
Endpoint | Functionality
------------ | -------------
POST /auth/register | Registers a new user
POST /auth/login | Login a user
POST /category_creation/ | Creates a new category
GET /category_view/ | Retrieves all created categories by that user
GET /category_byID/category_id | Retrieves a single category using it's ID
PUT /category_edit/category_id | Updates a category of a specified ID
DELETE /category_delete/category_id| Deletes a category of a specified ID
POST /create_recipe/category_id | Creates a new recipe in a category 
GET /view_recipes/category_id/ | Retrieves all created recipes in a category
GET /recipe_byid/category_id/recipe_id | Retrieves a single recipe using it's ID
PUT /recipe_edit/category_id/recipe_id | Updates a recipe in a category
DELETE /recipe_delete/category_id/recipe_id | Deletes a recipe in a category