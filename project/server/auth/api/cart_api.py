from flask import request, make_response, jsonify
from flask.views import MethodView
from sqlalchemy import inspect

from project.server.jwt_helper import token_required
from project.server.database import db
from project.server.models.cart_model import Cart
from project.server.models.cartItem_model import CartItem


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}
class GetCartAPI(MethodView):
    """
    Cart's information
    """
    @token_required
    def get(self, current_user):
        # check if cart already exist
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            responseObject = {
                'status': 'fail',
                'message': 'There arent any products in your cart. Try to add some ...'
            }
            return make_response(jsonify(responseObject)), 202
        else:
            try: 
                list_cart = CartItem.query.filter_by(cart_id=cart.id).all()
                data = [object_as_dict(item) for item in list_cart]
                # for item in data:
                #     cart.subtotal += item['subtotal']
                # cart.update_cash(cart.subtotal)
                # db.session.commit()
                responseObject = {
                    'status': 'success',
                    'data': {
                        "id": cart.id,
                        "cart_items": data,
                        "subtotal": cart.subtotal,
                        "total": cart.total,
                        "vat": cart.vat
                    }
                }
                return make_response(jsonify(responseObject), 200)
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
