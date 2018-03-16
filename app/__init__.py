from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
# this is a local import
from flask_cors import CORS
from instance.config import app_config
# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .categories import CATEGORIES_API
    app.register_blueprint(CATEGORIES_API)
    from .recipes import RECIPES_API
    app.register_blueprint(RECIPES_API)

    return app
