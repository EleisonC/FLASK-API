from flask import Blueprint 

# this instance of a Blueprint that represents the authentication blueprint
auth_blueprint = Blueprint('auth', __name__)

from . import views