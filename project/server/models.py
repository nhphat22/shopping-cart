import jwt
from sqlalchemy import Integer
# from project.server import app
from project.server.alchemy import db

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    firstName = db.Column(db.String(255))
    lastName = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False)

    def __init__(self, userName, password, firstname='', lastName='', email='email@gmail.com'):
        self.userName = userName
        # self.password = bcrypt.generate_password_hash(
        #     password, app.config.get('BCRYPT_LOG_ROUNDS')
        # ).decode()
        self.password = password
        self.firstname = firstname
        self.lastName = lastName
        self.email = email
       
    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'sub': user_id
            }
            return jwt.encode(
                payload,
                'SECRET_KEY',
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(
                auth_token, 
                'SECRET_KEY',
                algorithms='HS256'
            )
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

class Product(db.Model):
    """ Product Model for storing product related details """
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

class Cart(db.Model):
    """ Cart Model for storing cartItems and subtotal """
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cartItems = db.Column(db.ARRAY(Integer), nullable=False)
    total = db.Column(db.Float, nullable=False)
    vat = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    def __init__(self, cartItems):
        self.cartItems = cartItems
        self.total = sum(cartItems) #!!!!!
        self.vat = self.total * 0.1
        self.subtotal = self.total + self.vat
