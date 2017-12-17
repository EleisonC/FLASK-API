from . import auth_blueprint
import validator
from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User


class RegistrationView(MethodView):
    """This class registers a new user. """

    def post(self):
        """this class registers a new user."""

        user = User.query.filter_by(username=request.data['username']).first()

        if not user:
            # we will try to register them
            try:
                post_data = request.data
                # register the user
                username = post_data['username'].strip()
                password = post_data['password'].strip()
                if username and password:
                    if validator.validate_name(username) == "Valid Name" and\
                            validator.validate_password(password) == "Valid password":
                        user = User(username=username, password=password)
                        user.save()

                        response = {
                            'message': 'You registered successfully. Please log in.'
                        }
                        # return a response notifying the user that they registered well
                        return make_response(jsonify(response)), 201
                    else:
                        response = {
                            'message': 'Invalid username or password not strong enough. Please try again.'
                        }
                        return make_response(jsonify(response)), 403
            except Exception as e:
                # An error occured, therefore return a string message containg the error
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # there is an existing user. we dont want to register twice
            # return a message to the user telling them that they already exist
            response = {
                'message': 'User already exists. Please login'
            }

            return make_response(jsonify(response)), 202


class LoginView(MethodView):
    """This class-based view handles user login and access token generation. """

    def post(self):
        """Handle POST request for this view. Url --> /auth/login"""
        try:

            user = User.query.filter_by(
                username=request.data['username']).first()

            if user and user.password_is_valid(request.data['password']):
                # generate the access token.
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                # User does not exist. Hence an error message returnd
                response = {
                    'message': 'Invalid username or password, please try again'

                }
                return make_response(jsonify(response)), 401
        except Exception as e:
            # Create a response containing a string error message
            response = {
                'message': str(e)
            }
            # return a server error using the HTTP Error message
            return make_response(jsonify(response)), 500


class Logout(MethodView):
    """ This class logout a user"""

    def post(self):
        """ This method logout a user"""
        auth_header = request.headers.get("Authorization")
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if isinstance(user_id, int):
                user_id = User.decode_token(access_token)
                user = User.query.filter_by(id=user_id).first()

                if user:
                    user.tokken = ''
                    user.save()

                response = {
                    'message': 'Logged out Successfully'
                }
                return make_response(jsonify(response)), 200


class ResetPassword(MethodView):
    """ this class is to allow a user to reset password"""

    def put(self):
        """ this method is to allow a user to reset password"""
        auth_header = request.headers.get("Authorization")
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if isinstance(user_id, int):
                put_data = request.data
                username = put_data['username']
                password = put_data['password']
                new = put_data['new_password'].strip()
                confirm = put_data['confirm_password'].strip()

                reset_data = [new, confirm]
                user = User.query.filter_by(
                    username=username).first()

                if not user and not user.password_is_valid(password):
                    responce = jsonify({
                        'message': 'User not found or inccorect password'
                    })
                    return make_response(responce), 404
                if not all(reset_data):
                    responce = jsonify({
                        'message': 'Invalid data. Please try again.'
                    })
                    return make_response(responce)
                else:
                    if validator.validate_password_reset(
                            new, confirm) == "Valid password":
                        user.password = new
                        user.save()
                        response = {
                            'message': 'Password Succesfully Changed'}
                        return make_response(jsonify(response)), 200
                    else:
                        response = {
                            'message': "Passwords don't match or not strong"
                        }
                        return make_response(jsonify(response))


# define the API resource
registration_view = RegistrationView.as_view('register_view')
login_view = LoginView.as_view('login_view')
logout = Logout.as_view('logout_view')
reset = ResetPassword.as_view('reset_password')
# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint

auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])

# define the rule for the registration url --> /auth/login
# then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout,
    methods=['POST']
)

auth_blueprint.add_url_rule(
    '/auth/reset_password',
    view_func=reset,
    methods=['PUT']
)
