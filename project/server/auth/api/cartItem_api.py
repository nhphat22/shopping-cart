from flask import request, make_response, jsonify
from flask.views import MethodView

from project.server.database import db
from project.server.jwt_helper import token_required
from project.server.models.cart_model import Cart
from project.server.models.cartItem_model import CartItem
from project.server.models.product_model import Product

class AddToCartAPI(MethodView):
    """
    Add product and its quantity to user's cart
    """
    @token_required
    def post(self, current_user):
        post_data = request.get_json()
        # check if prouduct already exist
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            try:
                cart = Cart(
                    user_id = current_user.id,
                )
                # insert the user
                db.session.add(cart)
                db.session.commit()
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            product = Product.query.filter_by(name=post_data.get('product')).first()
            if not product:
                responseObject = {
                    'status': 'fail',
                    'message': 'We dont do that here. Choose another...'
                }
                return make_response(jsonify(responseObject)), 202
            else:
                try: 
                    cartItem = CartItem(
                        cart_id = cart.id,
                        product_id = product.id,
                        price = product.price,
                        quantity = post_data.get('quantity')
                    )
                    db.session.add(cartItem)
                    db.session.commit()
                    responseObject = {
                        'status': 'success',
                        'data' : {
                            'id': cartItem.id,
                            'name': product.name,
                            'quantity': post_data.get('quantity')
                        }
                    }
                    return make_response(jsonify(responseObject)), 201
                except Exception as e:
                    responseObject = {
                        'status': 'fail',
                        'message': 'Some error occurred. Please try again.'
                    }
                    return make_response(jsonify(responseObject)), 401

class UpdateQuantityAPI(MethodView):
    """
    Update quantity of a cart's item
    """
    @token_required
    def put(self, current_user, item_id):
        put_data = request.get_json()
        # check if prouduct already exist
        cartitem = CartItem.query.filter_by(id=item_id).first()
        try: 
            cartitem.update_quantity(put_data.get('quantity'))
            db.session.commit()
            responseObject = {
                'status': 'success',
                'data' : {
                    'id': cartitem.id,
                    'quantity': cartitem.quantity
                }
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401

class RemoveFromCartAPI(MethodView):
    """
    Remove an item from cart
    """
    @token_required
    def delete(self, current_user, item_id):
        try: 
            CartItem.query.filter_by(id=item_id).delete()
            # CartItem.query.filter(CartItem.id == item_id).delete()
            db.session.commit()
            responseObject = {
                'status': 'success',
                'message' : 'Removed'
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401
            