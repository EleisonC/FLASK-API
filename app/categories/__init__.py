from flask import Blueprint

# this instance of a Blueprint that represents the authentication blueprint
CATEGORIES_API = Blueprint('categories', __name__)

from . import views
