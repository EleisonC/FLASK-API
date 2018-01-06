from app import db
import jwt
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from flask import current_app


class User(db.Model):
    """This class represents the bucketlist table. """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String())
    category = db.relationship(
        'Category', order_by='Category.category_id', cascade='all, delete-orphan'
    )

    def __init__(self, username, password):
        """initialize with username and password"""
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """ Generate the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET
            jwt_string = jwt.encode(
                payload,
                "chris1234kal",
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            # return and error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """decode the token from the authorization header."""
        try:
            # try to decode the token using our secret variable
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistedToken.check_blacklist(
                auth_token=token)
            if is_blacklisted_token:
                return 'Expired token. Please log in'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return 'Expired token, Please login to get a new token'
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return 'Invalid token. Please register or login'


class Category(db.Model):
    """This class represents the bucketlist table. """
    __tablename__ = "category"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    recipe = db.relationship(
        'Recipe', order_by='Recipe.recipe_id', cascade='all, delete-orphan'
    )

    def __init__(self, category_name, created_by):
        """initialize with category name and created by"""
        self.category_name = category_name
        self.created_by = created_by

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """this method gets all the categories of foods for a given user."""
        # return Category.query.all()
        return Category.query.filter_by(created_by=user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Category: {}>".format(self.category_name)


class Recipe(db.Model):
    """this class represents the table of recipes"""
    __tablename__ = "recipe"

    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(255))
    instructions = db.Column(db.String())
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    category = db.Column(db.Integer, db.ForeignKey(Category.category_id))

    def __init__(self, recipe_name, instructions, category):
        """initialize with a recipe name"""
        self.recipe_name = recipe_name
        self.instructions = instructions
        self.category = category

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(category_id):
        """this method gets all the recipes of foods for a given category."""
        # return Recipe.query.all()
        return Recipe.query.filter_by(category=category_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Recipe: {}>".format(self.recipe_name)


class BlacklistedToken(db.Model):
    """ This table contains the table of blacklisted tokkens"""
    __tablename__ = "blacklist tokens"


    token_id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(
        db.DateTime, default=db.func.current_timestamp())

    def __init__(self, token):
        """ initialize with a token """
        self.token = token

    def save(self):
        """ save the token"""
        db.session.add(self)
        db.session.commit()
    @staticmethod
    def check_blacklist(auth_token):
        """function to check if token is blacklisted
        """
        # check whether token has been blacklisted
        res = BlacklistedToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
    def __repr__(self):
        return '<id: token: {}'.format(self.token)
