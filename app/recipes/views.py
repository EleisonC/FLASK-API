from . import RECIPES_API
from flask import request, jsonify, abort, make_response
from app.models import Category, Recipe, User
from flasgger import swag_from
import validator
from app.categories.views import authenticate
from sqlalchemy import desc

@RECIPES_API.route('/create_recipe/<int:category_id>', methods=["POST"])
@authenticate
@swag_from('/app/doc/create_recipe.yml')
def create_recipe(user_id, category_id, **kwargs):
    #this function is used to created a recipe under an existing category ID
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
                    "message": "Recipe has been created",
                    "recipe_id": recipe.recipe_id,
                    "recipe_name": recipe.recipe_name,
                    "instructions": recipe.instructions,
                    "date_created": recipe.date_created,
                    "date_modified": recipe.date_modified,
                    "category": recipe.category})
                response.status_code = 201
                return response
            return jsonify({'message': 'The Recipe Already Exists. Try another'}), 409
        return jsonify({'message': 'Invalid request'}), 400    
    return jsonify({'message': 'Enter valid data'}), 400
        


@RECIPES_API.route('/view_recipes/<int:category_id>/', methods=["GET"])
@swag_from('/app/doc/view_recipes.yml')
@authenticate
def view_all_recipes(user_id, category_id, **kwags):
    #this function is used to view all recipes under a category
    #the data can be paginated and also can search a specific category
    page, per_page = int(request.args.get('page', 1)), int(request.args.get('per_page', 3))
    q = str(request.args.get('q', '')).capitalize()
    name = Category.query.filter_by(category_id=category_id, created_by=user_id).first()
    if name:
        recipes = Recipe.query.filter_by(category=category_id).order_by(desc('date_created')).paginate(page, per_page, False)
        has_next=recipes.has_next
        has_prev=recipes.has_prev
        next_url = 'http://127.0.0.1:5000/view_recipes/' + str(category_id) + '/?page=' +\
            str(recipes.next_num)  if recipes.has_next else None
        prev_url = 'http://127.0.0.1:5000/view_recipes/' + str(category_id) + '/?page=' +\
            str(recipes.prev_num)  if recipes.has_prev else None

        result = []
        if q:
            recipes = Recipe.query.filter_by(category=category_id)
            for recipe in recipes:
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
            response = {
                "next_page": next_url,
                "previous_page": prev_url,
                "recipes":result,
                "has_next":has_next,
                "has_prev":has_prev
            }
            response = jsonify(response)
            response.status_code = 200
            return response
        else:
            result = []
            response = jsonify({
                'recipes': result,
                'message': 'no recipes available'})
            response.status_code = 200
            return response
    return jsonify({'message': 'Invalid request'}), 404

@RECIPES_API.route('/recipe_byid/<int:category_id>/<int:recipe_id>', methods=["GET", "POST"])
@swag_from('/app/doc/recipe_byID.yml')
@authenticate
def recipe_byid(user_id, category_id, recipe_id, **kwargs):
    #this function is used to view a recipe by ID under a category
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
@swag_from('/app/doc/recipe_edit.yml')
@authenticate
def recipe_manipulation(user_id, category_id, recipe_id, **kwargs):
    #this function is used to edit a recipe under a category
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
                        "message": "successfully edited " + recipe.recipe_name,
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
@swag_from('/app/doc/recipe_delete.yml')
@authenticate
def recipe_delete(user_id, category_id, recipe_id):
    # this function is used to delete a recipe
    name = Category.query.filter_by(category_id=category_id, created_by=user_id).first()
    if name:
        recipe = Recipe.query.filter_by(recipe_id=recipe_id).first()
        if not recipe:
            abort(404)
        else:
            recipe.delete()
            return {"message": "recipe {} deleted successfully".format(
                recipe.recipe_name)}, 200
    return jsonify({'message': 'Invalid request'})
