from . import auth_blueprint
import validator
from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User, BlacklistedToken
from flask_bcrypt import Bcrypt
from flasgger import swag_from
from app.categories.views import authenticate
class RegistrationView(MethodView):
    """This class registers a new user. """
    @swag_from('/app/doc/register_user.yml')
    def post(self):
        try:
            user = User.query.filter_by(email=request.data['email']).first()
            if not user:
                post_data = request.data
                # register the user
                email = post_data['email'].strip()
                username = post_data['username'].strip()
                password = post_data['password'].strip()
                if username and password and email:
                    
                    if validator.validate_name(username) != "Valid Name":
                        return jsonify({'message': 'please provide a valid username'})
                    if validator.validate_password(password) != "Valid password":
                         return jsonify({'message': 'please provide a strong valid password above six characters'})
                    if validator.validate_email(email) != "Valid email":
                        return jsonify({'message': 'please provide a valid email'})
                    user = User(username=username, password=password, email=email)
                    user.save()

                    response = {
                        'message': 'You registered successfully. Please log in.'
                    }
                    # return a response notifying the user that they registered well
                    return make_response(jsonify(response)), 201
                else:
                    return jsonify({'message': 'all fields required'})

            else:
                # there is an existing user. we dont want to register twice
                # return a message to the user telling them that they already exist
                response = {
                    'message': 'User already exists. Please choose another username'
                }

                return make_response(jsonify(response)), 202
        except Exception as e:
            # An error occured, therefore return a string message containg the error
            response = {
                'message': "Provide all the fields  in json form"
            }
            return make_response(jsonify(response)), 401

class LoginView(MethodView):
    """This class-based view handles user login and access token generation. """
    @swag_from('/app/doc/login_user.yml')
    def post(self):
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
                'message': "Provide both username and password"
            }
            # return a server error using the HTTP Error message
            return make_response(jsonify(response)), 500


class Logout(MethodView):
    """ This class logout a user"""
    @swag_from('/app/doc/logout_user.yml')
    def post(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({'message': 'Provide a token'})
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if isinstance(user_id, int):
                blacklist_token = BlacklistedToken(token=access_token)
                blacklist_token.save()
                return jsonify({'message': 'Logged out Successfully'})
            else:
                message = user_id
                response = {
                    'message': message
                }
                return jsonify(response), 401
        else:
            return jsonify({'message': 'please provide a  valid token'})

class ResetPassword(MethodView):
    """ this class is to allow a user to reset password"""
    @swag_from('/app/doc/change_user_password.yml')
    def put(self):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({'message': 'Provide a token'})
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
                if user and user.password_is_valid(password):
                    if not all(reset_data):
                        responce = jsonify({
                        'message': 'Invalid data. Please try again.'
                        })
                        return make_response(responce)
                    else:
                        if validator.validate_password_reset(
                                new, confirm) == "Valid password":
                            user.password = Bcrypt().generate_password_hash(new).decode()
                            user.save()
                            response = {'message': 'Password Succesfully Changed'}
                            return make_response(jsonify(response)), 200
                        return make_response(jsonify({
                            'message': "Passwords don't match or not strong"}))
                return jsonify({'message': 'Wrong username or password'})

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
