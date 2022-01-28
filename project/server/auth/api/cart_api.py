from flask import request, make_response, jsonify
from flask.views import MethodView

from project.server.jwt_helper import token_required
from project.server.models.cart_model import Cart

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
                responseObject = {
                    'status': 'success',
                    'data' : {
                        'id': cart.id,
                        'subtotal' : cart.subtotal,
                        'total': cart.total,
                        'vat': cart.vat
                    }
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
