from flask import Blueprint
from project.server.auth.api.user_api import RegisterAPI, LoginAPI, LogoutAPI
from project.server.auth.api.product_api import AddProductAPI
from project.server.auth.api.cart_api import GetCartAPI

auth_blueprint = Blueprint('auth', __name__)

# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
logout_view = LogoutAPI.as_view('logout_api')
product_view = AddProductAPI.as_view('product_api')
cart_view = GetCartAPI.as_view('getcart_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/product',
    view_func=product_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/cart',
    view_func=cart_view,
    methods=['GET']
)