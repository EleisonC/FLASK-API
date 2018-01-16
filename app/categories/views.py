from . import CATEGORIES_API
from flask import request, jsonify, abort, make_response
from app.models import Category, Recipe, User
import validator
from flasgger import swag_from
from functools import wraps


def authenticate(func):
    @wraps(func)
    def auth(*args, **kwargs):
        
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Provide a token'})
        access_token = auth_header.split(" ")[1]

        if access_token:

            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                return func(user_id, *args, **kwargs)
            else:
                message = user_id
            response = {
                'message': message
            }
            return jsonify(response), 401
        return jsonify({'message': 'please login.'})
    return auth
        
@CATEGORIES_API.route('/category_creation/', methods=["POST"])
@swag_from('/app/doc/create_category.yml')
@authenticate
def create_category(user_id):
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

@CATEGORIES_API.route('/category_view/', methods=["GET"])
@swag_from('/app/doc/category_view.yml')
@authenticate
def fetch_category(user_id):
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    q = str(request.args.get('q', '')).capitalize()
    categories = Category.query.filter_by(
        created_by=user_id).paginate(page, per_page, False)
    result = []
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
                result.append(obj)
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

@CATEGORIES_API.route('/category_delete/<int:category_id>', methods=["DELETE"])
@swag_from('/app/doc/category_delete.yml')
@authenticate
def category_delete(user_id, category_id, **kwargs):
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

@CATEGORIES_API.route('/category_edit/<int:category_id>', methods=["PUT"])
@swag_from('/app/doc/category_edit.yml')
@authenticate
def category_manipulation(user_id, category_id, **kwargs):
    category = Category.query.filter_by(created_by=user_id,
                                        category_id=category_id).first()
    if category:
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
    else:
        return jsonify({'message': 'Category does not exist'})

@CATEGORIES_API.route('/category_byID/<int:category_id>', methods=["GET"])
@swag_from('/app/doc/category_byID.yml')
@authenticate
def category_view(user_id, category_id, **kwargs):
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
