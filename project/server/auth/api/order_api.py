from flask import request, make_response, jsonify
from flask.views import MethodView

from project.server.database import db
from project.server.jwt_helper import token_required
from project.server.models.order_model import Order
from project.server.models.cart_model import Cart

class CreateOrderAPI(MethodView):
    """
    """
    @token_required
    def post(self, current_user, cart_id):
        # get the post data
        cart = Cart.query.filter_by(id=cart_id).first()
        if not cart:
            responseObject = {
                'status': 'fail',
                'message': 'There arent any products in your cart. Try to add some ...'
            }
            return make_response(jsonify(responseObject)), 202
        else:
            try:
                order = Order(
                    cart_id=cart_id,
                    amount=cart.total
                )
                print(order.status)
                # insert the user
                db.session.add(order)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'data': {
                        "id": order.id,
                        "amount": order.amount
                    }
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
       