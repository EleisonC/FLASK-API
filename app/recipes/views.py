from . import RECIPES_API
from flask import request, jsonify, abort, make_response
from app.models import Category, Recipe, User
import validator
from app.categories.views import authenticate

@RECIPES_API.route('/create_recipe/<int:category_id>', methods=["POST"])
@authenticate
def create_recipe(user_id, category_id, **kwargs):
    recipe_name = str(request.data.get('recipe_name')).strip()
    instructions = str(request.data.get('instructions')).strip()
    if recipe_name and instructions:
        recipe_name = recipe_name.capitalize()
        name = Category.query.filter_by(category_id=category_id, created_by=user_id).first()
        if name:
            name2 = Recipe.query.filter_by(category=category_id, recipe_name=recipe_name).first()
            if name2 is None:
                recipe = Recipe(recipe_name=recipe_name,instructions=instructions,
                                category=category_id)
                recipe.save()
                response = jsonify({
                    "recipe_id": recipe.recipe_id,
                    "recipe_name": recipe.recipe_name,
                    "instructions": recipe.instructions,
                    "date_created": recipe.date_created,
                    "date_modified": recipe.date_modified,
                    "category": recipe.category})
                response.status_code = 201
                return response
            return jsonify({'message': 'The name already exists. Try another'})
        return jsonify({'message': 'Invalid request'})     
    return jsonify({'message': 'Enter valid data'})
        


@RECIPES_API.route('/view_recipes/<int:category_id>/', methods=["GET"])
@authenticate
def view_all_recipes(user_id, category_id, **kwags):
    page, per_page = int(request.args.get('page', 1)), int(request.args.get('per_page', 5))
    q = str(request.args.get('q', '')).capitalize()
    name = Category.query.filter_by(category_id=category_id, created_by=user_id).first()
    if name:
        recipes = Recipe.query.filter_by(category=category_id).paginate(page, per_page, False)
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
                else:
                    response = jsonify({'meassage': 'recipie not found'})
                    response.status_code = 401
                    return response
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
            response = jsonify({'message': 'no recipes available'})
            response.status_code = 404
            return response
    return jsonify({'message': 'Invalid request'})

@RECIPES_API.route('/recipe_byid/<int:category_id>/<int:recipe_id>', methods=["GET", "POST"])
@authenticate
def recipe_byid(user_id, category_id, recipe_id, **kwargs):
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

@RECIPES_API.route('/recipe_edit/<int:category_id>/<int:recipe_id>', methods=["PUT"])
@authenticate
def recipe_manipulation(user_id, category_id, recipe_id, **kwargs):
    name = Category.query.filter_by(category_id=category_id, created_by=user_id).first()
    if name:
        recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
        if not recipe:
            return jsonify({'message': 'this recipe does not exist'})
        if request.method == "PUT":
            name = str(request.data.get('recipe_name', '')).strip()
            instructions = str(request.data.get('instructions', '')).strip()
            if name and instructions:
                name, name2 = name.capitalize(), Recipe.query.filter_by(recipe_name=name).first()
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
                return jsonify({'message': ''})
            return jsonify({'message': 'Enter valid data'})
    return jsonify({'message': 'Invalid request'})

@RECIPES_API.route('/recipe_delete/<int:category_id>/<int:recipe_id>', methods=["DELETE"])
@authenticate
def recipe_delete(user_id, category_id, recipe_id):
    name = Category.query.filter_by(category_id=category_id, created_by=user_id).first()
    if name:
        recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
        if not recipe:
            abort(404)
        else:
            # if the method is a DELETE request
            recipe.delete()
            return {"message": "recipe {} deleted successfully".format(
                recipe.recipe_id)}, 200
    return jsonify({'message': 'Invalid request'})
