from . import RECIPES_API
from flask import request, jsonify, abort, make_response
from app.models import Category, Recipe, User
import validator


@RECIPES_API.route('/create_recipe/<int:category_id>', methods=["POST"])
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

@RECIPES_API.route('/view_all_recipes/<int:category_id>/', methods=["GET"])
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

@RECIPES_API.route('/recipe_byid/<int:category_id>/<int:recipe_id>', methods=["GET", "POST"])
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

@RECIPES_API.route('/recipe_manipulation/<int:category_id>/<int:recipe_id>', methods=["PUT"])
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
@RECIPES_API.route('/recipe_manipulation/<int:category_id>/<int:recipe_id>', methods=["DELETE"])
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