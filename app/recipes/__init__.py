from flask import Blueprint

# this instance of a Blueprint that represents the authentication blueprint
RECIPES_API = Blueprint('recipes', __name__)

from . import views