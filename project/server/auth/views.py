from flask import Blueprint
from project.server.auth.api.user_api import RegisterAPI, LoginAPI, LogoutAPI
from project.server.auth.api.product_api import AddProductAPI
from project.server.auth.api.cart_api import GetCartAPI
from project.server.auth.api.cartItem_api import AddToCartAPI, UpdateQuantityAPI, RemoveFromCartAPI
from project.server.auth.api.order_api import CreateOrderAPI


auth_blueprint = Blueprint('auth', __name__)

# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
logout_view = LogoutAPI.as_view('logout_api')
product_view = AddProductAPI.as_view('product_api')
add_view = AddToCartAPI.as_view('add_api')
update_view = UpdateQuantityAPI.as_view('update_api')
remove_view = RemoveFromCartAPI.as_view('remove_api')
cart_view = GetCartAPI.as_view('getcart_api')
create_view = CreateOrderAPI.as_view('createorder_api')

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
    '/auth/add',
    view_func=add_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/update/<item_id>',
    view_func=update_view,
    methods=['PUT']
)
auth_blueprint.add_url_rule(
    '/auth/remove/<item_id>',
    view_func=remove_view,
    methods=['DELETE']
)
auth_blueprint.add_url_rule(
    '/auth/cart',
    view_func=cart_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/auth/<cart_id>/create',
    view_func=create_view,
    methods=['POST']
)