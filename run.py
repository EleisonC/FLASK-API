import os
from app import create_app
from instance.config import app_config
from flasgger import Swagger
from flask import render_template, redirect, jsonify
config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)


swag = Swagger(app,
               template={
                   "info": {
                       "title": "Yummy Recipes CK",
                       "description": """An application
                        that can help one keep track of food categories and recipes""",
                       "securityDefinitions": {
                           "TokenHeader": {
                               "type": "apiKey",
                               "name": "Authorization",
                               "in": "header"
                           }
                       }
                   }
               })

@app.route("/")
def main():
    return redirect('/apidocs')

if __name__ == '__main__':
    app.run()
