from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
#this is a local import 
from instance.config import app_config

POSTGRES = {
    'user': 'postgres',
    'pw': 'chrisenlarry',
    'db': 'yummys',
    'host': 'localhost',
    'port': '5432'
}
#initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config['development'])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)
    

    return app