from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User

class RegistrationView(MethodView):
    """This class registers a new user. """

    def post(self):
        """this class registers a new user."""

        user = User.query.filter_by(username=request.data['username']).first()

        if not user:
            #we will try to register them
            try:
                post_data = request.data
                #register the user
                username = post_data['username']
                password = post_data['password']
                user = User(username=username, password=password)
                user.save()

                response = {
                    'message': 'You registered successfully. Please log in.'
                }
                #return a response notifying the user that they registered well
                return make_response(jsonify(response)), 201
            except Exception as e:
                #An error occured, therefore return a string message containg the error
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            #there is an existing user. we dont want to register twice
            #return a message to the user telling them that they already exist
            response = {
                'message': 'User already exists. Please login'
            }

            return make_response(jsonify(response)), 202

registration_view = RegistrationView.as_view('register_view')

# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint

auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])