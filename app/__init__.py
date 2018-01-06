from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
# this is a local import
from instance.config import app_config
from flask import request, jsonify, abort, make_response
import validator
"""POSTGRES = {
    'user': 'postgres',
    'pw': 'chrisenlarry',
    'db': 'yummys',
    'host': 'localhost',
    'port': '5432'
}"""
# initialize sql-alchemy

db = SQLAlchemy()


def create_app(config_name):
    from app.models import Category, Recipe, User
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    @app.route('/category_creation/', methods=["POST"])
    def create_category():
        """
        Create categories
        ---
        tags:
          - category function
        parameters:
          - in: body
            name: body
            required: True
            type: string
            description: enter data in json format
        security:
          - TokenHeader: []
        responses:
            200:
              description: category successfully created
            201:
              description: You successfully registered
              schema:
                id: Register
                properties:
                  name:
                    type: string
                    default: Lunch
            400:
              description: name must not contain special characters and should not contain numbers only
              schema:
                id: Register User
                properties:
                  name:
                    type: string
                    default: Invalid json data
            422:
              description: If nothing is entered
              schema:
                id: Add category
                properties:
                  name:
                    type: string
                    default: ""

        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:

            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):

                category_name = str(request.data.get(
                    'category_name', '')).strip()
                if category_name:
                    category_name = category_name.capitalize()
                    name2 = Category.query.filter_by(created_by=user_id, category_name=category_name).first()
                    if name2 is None:
                        if validator.validate_name(category_name) != "Valid Name":
                            return jsonify({'message': 'name must not contain special charaters'}), 400
                        category = Category(category_name=category_name,
                                            created_by=user_id)
                        category.save()
                        response = jsonify({
                            'category_id': category.category_id,
                            'category_name': category.category_name,
                            'date_created': category.date_created,
                            'data_modified': category.date_modified,
                            'created_by': user_id
                        })
                        response.status_code = 201
                        return response
                    else:
                        return jsonify({'message': 'The name already exists. Try another'})
                else:
                    return jsonify({'message': 'Enter valid data'}), 422
            else:
                message = user_id
                response = {
                    'message': message
                }
                return jsonify(response), 401

    @app.route('/category_view_all/', methods=["GET"])
    def fetch_category():
        """
        Get categories
        ---
        tags:
          - category function
        parameters:
          - in: query
            name: q
            required: True
            type: string
            description: Query category by name
          - in: query
            name: page
            required: True
            type: integer
            description: the page to be displayed
          - in: query
            name: per page
            required: True
            type: integer
            description: number of items displayed per page
        security:
          - TokenHeader: []
        responses:
            200:
              description:  category successfully created
            201:
              description: You successfully registered
              schema:
                id: Register
                properties:
                  name:
                    type: string
                    default: Lunch
            400:
              description: name must not contain special characters and should not contain numbers only
              schema:
                id: Register User
                properties:
                  name:
                    type: string
                    default: Invalid json data
            422:
              description: If nothing is entered
              schema:
                id: Add category
                properties:
                  name:
                    type: string
                    default: ""

        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:

            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                page = int(request.data.get('page', 1))
                per_page = int(request.data.get('per_page', 5))
                q = str(request.data.get('q', '')).capitalize()
                categories = Category.query.filter_by(
                    created_by=user_id).paginate(page=page, per_page=per_page)
                result = []
                if categories:
                    if q:
                        for category in categories.items:
                            if q in category.category_name:
                                obj = {
                                    'category_id': category.category_id,
                                    'category_name': category.category_name,
                                    'date_created': category.date_created,
                                    'data_modified': category.date_modified,
                                    'created_by': user_id
                                }
                                response = jsonify(obj)
                                response.status_code = 200
                                return response
                            else:
                                responce = jsonify({
                                    'meassage': 'category not found'
                                })
                                responce.status_code = 404
                                return responce
                    else:
                        for category in categories.items:
                            obj = {
                                'category_id': category.category_id,
                                'category_name': category.category_name,
                                'date_created': category.date_created,
                                'data_modified': category.date_modified,
                                'created_by': user_id
                            }
                            result.append(obj)
                            # return jsonify(result)
                        if result:
                            response = jsonify(result)
                            response.status_code = 200
                            return response
                        else:
                            response = jsonify({
                                'message': 'no categories available'
                            })
                            response.status_code = 404
                            return response
                else:
                    return jsonify({'message': 'Invalid request'})        
            else:
                message = user_id
                response = {
                    'message': message
                }
                return jsonify(response), 401

    @app.route('/category_manipulation/<int:category_id>',
               methods=["DELETE"])
    def category_delete(category_id, **kwargs):
        """
        Deletes a category
        ---
        tags:
         - category function
        parameters:
         - in: path
           name: category_id
           required: True
           type: integer
           description: Delete a category using an id
        security:
         - TokenHeader: []
        responses:
            200:
              description:  category successfully deleted
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:

            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                category = Category.query.filter_by(created_by=user_id,
                                                    category_id=category_id).first()
                if not category:
                    return jsonify({'message': 'Invalid request'})
                if request.method == 'DELETE':
                    category.delete()
                    return {
                        "message": "catergory {} deleted successfully".format(
                            category.category_id)
                    }, 200
    @app.route('/category_manipulation/<int:category_id>',
               methods=["PUT"])
    def category_manipulation(category_id, **kwargs):
        """
        update a category
        ---
        tags:
         - category function
        parameters:
         - in: path
           name: category_id
           required: True
           type: string
           description: the category_id of category to update
         - in: body
           name: new category name
           required: True
           type: integer
           description: this is the new name the category will change to.
        security:
         - TokenHeader: []
        responses:
            200:
             description:  category successfully created
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:

            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                category = Category.query.filter_by(created_by=user_id,
                                                    category_id=category_id).first()
                if not category:
                    return jsonify({'message': 'Invalid request'})
                if request.method == 'PUT':
                    name = str(request.data.get('category_name', '')).strip()
                    if name:
                        name = name.capitalize()
                        name2 = Category.query.filter_by(category_name=name).first()
                        if name2 is None:
                            category.category_name = name
                            category.save()
                            response = jsonify({
                                'category_id': category.category_id,
                                'category_name': category.category_name,
                                'date_created': category.date_created,
                                'data_modified': category.date_modified,
                                'created_by': category.created_by

                            })
                            response.status_code = 200
                            return response
                        else:
                            return jsonify({'message': 'The name already exists. Try another'})
                    else:
                        return jsonify({'message': 'please put valid data'})
    @app.route('/category_manipulation/<int:category_id>',
               methods=["GET"])
    def category_view(category_id, **kwargs):
        """
        Get a category by id
        ---
        tags:
         - category function
        parameters:
         - in: path
           name: category_id
           required: True
           type: string
           description: the category_id of category to be viewed
        security:
         - TokenHeader: []
        responses:
            200:
              description:  category successfully created
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:

            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                category = Category.query.filter_by(created_by=user_id,
                                                    category_id=category_id).first()
                if not category:
                    return jsonify({'message': 'Invalid request'})
                else:
                    # for the get method
                    response = jsonify({
                        'category_id': category.category_id,
                        'category_name': category.category_name,
                        'date_created': category.date_created,
                        'date_modified': category.date_modified,
                        'created_by': category.created_by
                    })
                    response.status_code = 200
                    return response
            else:
                message = user_id
                response = {
                    'message': message
                }
                return jsonify(response), 401

    @app.route('/create_recipe/<int:category_id>', methods=["POST"])
    def create_recipe(category_id, **kwargs):
        """
        Create recipes
        ---
        tags:
         - recipe function
        parameters:
         - in: path
           name: category_id
           required: True
           type: integer
           description: the id of the category the recipe will belong to
         - in: body
           name: body
           required: True
           type: string
           description: enter recipe name and intsructions
        security:
         - TokenHeader: []
        responses:
            200:
              description:  recipe successfully created
            201:
              description: You successfully created a recipe
              schema:
                id: Register
                properties:
                  name:
                    type: string
                    default: Lunch
            400:
              description: name must not contain special characters and should not contain numbers only
              schema:
                id: Register User
                properties:
                  name:
                    type: string
                    default: Invalid json data
            422:
              description: If nothing is entered
              schema:
                id: Add category
                properties:
                  name:
                    type: string
                    default: ""

        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:

            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                recipe_name = str(request.data.get('recipe_name')).strip()
                instructions = str(request.data.get('instructions')).strip()
                if recipe_name and instructions:
                    recipe_name = recipe_name.capitalize()
                    name = Category.query.filter_by(category_id=category_id, created_by=user_id).first()
                    if name:
                        name2 = Recipe.query.filter_by(category=category_id, recipe_name=recipe_name).first()
                        if name2 is None:
                            recipe = Recipe(recipe_name=recipe_name,
                                            instructions=instructions,
                                            category=category_id)
                            recipe.save()
                            response = jsonify({
                                "recipe_id": recipe.recipe_id,
                                "recipe_name": recipe.recipe_name,
                                "instructions": recipe.instructions,
                                "date_created": recipe.date_created,
                                "date_modified": recipe.date_modified,
                                "category": recipe.category
                            })
                            response.status_code = 201
                            return response
                        else:
                            return jsonify({'message': 'The name already exists. Try another'})
                    else:
                        return jsonify({'message': 'Invalid request'})
                else:
                    return jsonify({'message': 'Enter valid data'})
        else:
            message = user_id
            response = {
                'message': message
            }
            return jsonify(response), 401

    @app.route('/view_all_recipes/<int:category_id>/', methods=["GET"])
    def view_all_recipes(category_id, **kwags):
        """
        View recipes of a specific category or query on specific recipe
        ---
        tags:
         - recipe function
        parameters:
         - in: path
           name: category_id
           required: True
           type: integer
           description: the id of the category the recipe will belong to
         - in: query
           name: query
           required: True
           type: string
           description: enter recipe name
         - in: query
           name: page
           required: True
           type: integer
           description: page to be diplayed
         - in: query
           name: per page
           required: True
           type: integer
           description: number of items to be displayed per page
        security:
         - TokenHeader: []
        responses:
            200:
              description:  category successfully created
            201:
              description: You successfully registered
              schema:
                id: Register
                properties:
                  name:
                    type: string
                    default: Lunch
            404:
              description: recipe not found
              schema:
                id: Register User
                properties:
                  name:
                    type: string
                    default: Invalid json data

        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:

            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                page = int(request.data.get('page', 1))
                per_page = int(request.data.get('per_page', 5))
                q = str(request.data.get('q', ''))
                name = Category.query.filter_by(category_id=category_id, created_by=user_id).first()
                if name:
                    recipes = Recipe.query.filter_by(
                        category=category_id).paginate(page=page, per_page=per_page)
                    result = []
                    if q:
                        for recipe in recipes.items:
                            if q in recipe.recipe_name:
                                obj = {
                                    "recipe_id": recipe.recipe_id,
                                    "recipe_name": recipe.recipe_name,
                                    "instructions": recipe.instructions,
                                    "date_created": recipe.date_created,
                                    "date_modified": recipe.date_modified,
                                    "category": recipe.category
                                }
                                result.append(obj)
                                response = jsonify(result)
                                response.status_code = 200
                                return response
                            else:
                                response = jsonify({
                                    'meassage': 'category not found'
                                })
                                response.status_code = 401
                                return response
                    else:
                        for recipe in recipes.items:
                            obj = {
                                "recipe_id": recipe.recipe_id,
                                "recipe_name": recipe.recipe_name,
                                "instructions": recipe.instructions,
                                "date_created": recipe.date_created,
                                "date_modified": recipe.date_modified,
                                "category": recipe.category
                            }
                            result.append(obj)
                        if result:
                            response = jsonify(result)
                            response.status_code = 200
                            return response
                        else:
                            response = jsonify({
                                'message': 'no recipes available'
                            })
                            response.status_code = 404
                            return response
                else:
                    return jsonify({'message': 'Invalid request'})
            else:
                message = user_id
                response = {
                    'message': message
                }
                return jsonify(response), 401

    @app.route('/recipe_byid/<int:category_id>/<int:recipe_id>',
               methods=["GET", "POST"])
    def recipe_byid(category_id, recipe_id, **kwargs):
        """
        View recipes of a specific category or query on specific recipe
        ---
        tags:
         - recipe function
        parameters:
         - in: path
           name: category_id
           required: True
           type: integer
           description: the id of the category the recipe will belong to
         - in: path
           name: recipe_id
           required: True
           type: integer
           description: enter recipe id that will be returned
        security:
         - TokenHeader: []
        responses:
            200:
              description:  category successfully created
            201:
              description: You successfully registered
              schema:
                id: Register
                properties:
                  name:
                    type: string
                    default: Lunch
            404:
              description: recipe not found
              schema:
                id: Register User
                properties:
                  name:
                    type: string
                    default: Invalid json data

        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:

            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                name = Category.query.filter_by(category_id=category_id, created_by=user_id).first()
                if name:
                    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
                    if not recipe:
                        abort(404)
                    response = jsonify({
                        "recipe_id": recipe.recipe_id,
                        "recipe_name": recipe.recipe_name,
                        "instructions": recipe.instructions,
                        "date_created": recipe.date_created,
                        "date_modified": recipe.date_modified,
                        "category": recipe.category
                    })
                    response.status_code = 200
                    return response
                else:
                    return jsonify({'message': 'Invalid request'})
            else:
                message = user_id
                response = {
                    'message': message
                }
                return jsonify(response), 401

    @app.route('/recipe_manipulation/<int:category_id>/<int:recipe_id>',
               methods=["PUT"])
    def recipe_manipulation(category_id, recipe_id, **kwargs):
        """
        update a recipe
        ---
        tags:
         - recipe function
        parameters:
         - in: path
           name: category_id
           required: True
           type: string
           description: the category_id of category to update
         - in: path
           name: recipe_id
           required: True
           type: string
           description: the recipe id of recipe to update
         - in: body
           name: body
           required: True
           type: string
           description: this contains the update name and instructions for the recipe
        security:
         - TokenHeader: []
        responses:
            200:
              description:  recipe successfully updated
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:

            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                name = Category.query.filter_by(category_id=category_id, created_by=user_id).first()
                if name:
                    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
                    if not recipe:
                        abort(404)

                    if request.method == "PUT":
                        name = str(request.data.get('recipe_name', '')).strip()
                        instructions = str(request.data.get('instructions', '')).strip()
                        if name and instructions:
                            name = name.capitalize()
                            name2 = Recipe.query.filter_by(recipe_name=name).first()
                            if name2 is None:
                                recipe.recipe_name = name
                                recipe.instructions = instructions
                                recipe.save()
                                response = jsonify({
                                    "recipe_id": recipe.recipe_id,
                                    "recipe_name": recipe.recipe_name,
                                    "instructions": recipe.instructions,
                                    "date_created": recipe.date_created,
                                    "date_modified": recipe.date_modified,
                                    "category": recipe.category
                                })
                                response.status_code = 200
                                return response
                            else:
                                return jsonify({'message': ''})
                        else:
                            return jsonify({'message': 'Enter valid data'})
                else:
                    return jsonify({'message': 'Invalid request'})
            else:
                message = user_id
                response = {
                    'message': message
                }
                return jsonify(response), 401
    @app.route('/recipe_manipulation/<int:category_id>/<int:recipe_id>',
               methods=["DELETE"])
    def recipe_delete(category_id, recipe_id):
        """
        Deletes a recipe
        ---
        tags:
         - recipe function
        parameters:
         - in: path
           name: category_id
           required: True
           type: integer
           description: category of the recipe that will be deleted
         - in: path
           name: recipe_id
           required: True
           type: integer
           description: recipe id for the recpie to be deleted
        security:
         - TokenHeader: []
        responses:
            200:
              description:  category successfully deleted
        """
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:

            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                name = Category.query.filter_by(category_id=category_id, created_by=user_id).first()
                if name:
                    recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
                    if not recipe:
                        abort(404)
                    else:
                        # if the method is a DELETE request
                        recipe.delete()
                        return {
                            "message": "recipe {} deleted successfully".format(
                                recipe.recipe_id)
                        }, 200
                else:
                    return jsonify({'message': 'Invalid request'})
            else:
                message = user_id
                response = {
                    'message': message
                }
                return jsonify(response), 401

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
