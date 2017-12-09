from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
#this is a local import 
from instance.config import app_config
from flask import request, jsonify, abort

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
    from app.models import Category, Recipe
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    
    @app.route('/category_creation/', methods=["POST"])
    def create_category():
        category_name = str(request.data.get('category_name', ''))
        if category_name:
            category = Category(category_name=category_name)
            category.save()
            response = jsonify({
                'id': category.id,
                'category_name': category.category_name,
                'date_created': category.date_created,
                'data_modified': category.date_modified
            })
            response.status_code = 201
            return response 
    @app.route('/category_view_all/', methods=["GET","POST"])
    def fetch_category():
        categories = Category.get_all()
        
        result = []

        for category in categories:
            
            obj={
                'id': category.id,
                'category_name': category.category_name,
                'date_created': category.date_created,
                'data_modified': category.date_modified
            }
            result.append(obj)

        response = jsonify(result)
        response.status_code = 200
        return response
    
    @app.route('/category_manipulation/<int:id>', methods=["GET","PUT","DELETE"])
    def category_manipulation(id, **kwargs):
        #this is to retrieve a category using it's ID
        category = Category.query.filter_by(id=id).first()
        if not category:
            #raise a 404 status code if resource not found
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
                'data_modified': category.date_modified

            })
            response.status_code = 200 
            return response
        else:
            #for the get method
            response = jsonify({
                'id': category.id,
                'category_name': category.category_name,
                'date_created': category.date_created,
                'date_modified': category.date_modified
            })
            response.status_code = 200
            return response
    
    @app.route('/create_recipe/', methods=["POST"])
    def create_recipe():
        recipe_name = str(request.data.get('recipe_name'))  
        instructions = str(request.data.get('instructions'))
        if recipe_name and instructions:
            recipe = Recipe(recipe_name=recipe_name, instructions=instructions)
            recipe.save()
            response= jsonify({
                "id":recipe.id,
                "recipe_name":recipe.recipe_name,
                "instructions":recipe.instructions,
                "date_created":recipe.date_created,
                "date_modified":recipe.date_modified
            })
            response.status_code = 201
            return response     

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app

