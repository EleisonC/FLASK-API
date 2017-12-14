from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
# this is a local import
from instance.config import app_config
from flask import request, jsonify, abort, make_response

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
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    @app.route('/category_creation/', methods=["POST"])
    def create_category():
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:

            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):

                category_name = str(request.data.get('category_name', ''))
                if category_name:
                    category = Category(category_name=category_name,
                                        created_by=user_id)
                    category.save()
                    response = jsonify({
                        'id': category.id,
                        'category_name': category.category_name,
                        'date_created': category.date_created,
                        'data_modified': category.date_modified,
                        'created_by': user_id
                    })
                    response.status_code = 201
                    return response
        else:
            message = user_id
            response = {
                'message': message
            }
            return jsonify(response), 401

    @app.route('/category_view_all/', methods=["GET", "POST"])
    def fetch_category():
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:

            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                categories = Category.query.filter_by(created_by=user_id)

                result = []

                for category in categories:

                    obj = {
                        'id': category.id,
                        'category_name': category.category_name,
                        'date_created': category.date_created,
                        'data_modified': category.date_modified,
                        'created_by': user_id
                    }
                    result.append(obj)

                response = jsonify(result)
                response.status_code = 200
                return response
        else:
            message = user_id
            response = {
                'message': message
            }
            return jsonify(response), 401

    @app.route('/category_manipulation/<int:id>', methods=["GET", "PUT", "DELETE"])
    def category_manipulation(id, **kwargs):
        # this is to retrieve a category using it's ID
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:

            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                category = Category.query.filter_by(id=id).first()
                if not category:
                    # raise a 404 status code if resource not found
                    abort(404)

                if request.method == 'DELETE':
                    category.delete()
                    return {
                        "message": "catergory {} deleted successfully".format(category.id)
                    }, 200

                elif request.method == 'PUT':
                    name = str(request.data.get('category_name', ''))
                    category.category_name = name
                    category.save()
                    response = jsonify({
                        'id': category.id,
                        'category_name': category.category_name,
                        'date_created': category.date_created,
                        'data_modified': category.date_modified,
                        'created_by': category.created_by

                    })
                    response.status_code = 200
                    return response
                else:
                    # for the get method
                    response = jsonify({
                        'id': category.id,
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

    @app.route('/create_recipe/<int:id>', methods=["POST"])
    def create_recipe(category_id):
        """ method to create a recipe."""
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:

            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                recipe_name = str(request.data.get('recipe_name'))
                instructions = str(request.data.get('instructions'))
                if recipe_name and instructions:
                    recipe = Recipe(recipe_name=recipe_name,
                                    instructions=instructions,
                                    category=category_id)
                    recipe.save()
                    response = jsonify({
                        "id": recipe.id,
                        "recipe_name": recipe.recipe_name,
                        "instructions": recipe.instructions,
                        "date_created": recipe.date_created,
                        "date_modified": recipe.date_modified,
                        "category": recipe.category
                    })
                    response.status_code = 201
                    return response
        else:
            message = user_id
            response = {
                'message': message
            }
            return jsonify(response), 401

    @app.route('/view_all_recipes/', methods=["POST", "GET"])
    def view_all_recipes():
        recipes = Recipe.get_all()
        print(recipes)
        result = []
        for recipe in recipes:
            obj = {
                "id": recipe.id,
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

    @app.route('/recipe_byid/<int:id>', methods=["GET", "POST"])
    def recipe_byid(id, **kwargs):
        # This is to retrieve a specific recipe by id
        recipe = Recipe.query.filter_by(id=id).first()
        if not recipe:
            abort(404)
        response = jsonify({
            "id": recipe.id,
            "recipe_name": recipe.recipe_name,
            "instructions": recipe.instructions,
            "date_created": recipe.date_created,
            "date_modified": recipe.date_modified,
            "category": recipe.category
        })
        response.status_code = 200
        return response

    @app.route('/recipe_manipulation/<int:id>', methods=["PUT", "DELETE"])
    def recipe_manipulation(id, **kwargs):
        recipe = Recipe.query.filter_by(id=id).first()
        if not recipe:
            abort(404)

        if request.method == "PUT":
            name = str(request.data.get('recipe_name', ''))
            instructions = str(request.data.get('instructions', ''))
            recipe.recipe_name = name
            recipe.instructions = instructions
            recipe.save()
            response = jsonify({
                "id": recipe.id,
                "recipe_name": recipe.recipe_name,
                "instructions": recipe.instructions,
                "date_created": recipe.date_created,
                "date_modified": recipe.date_modified,
                "category": recipe.category
            })
            response.status_code = 200
            return response
        else:
            # if the method is a DELETE request
            recipe.delete()
            return {
                "message": "recipe {} deleted successfully".format(recipe.id)
            }, 200

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
