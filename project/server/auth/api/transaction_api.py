from socket import herror
from flask import make_response, jsonify
from flask.views import MethodView
import requests
from hashlib import md5
import hmac
import json

from project.server.jwt_helper import encode_merchant_token, decode_merchant_token
from project.server.database import db
from project.server.config import BaseConfig
from project.server.jwt_helper import token_required
from project.server.models.cart_model import Cart
from project.server.models.order_model import Order


class PaymentAPI(MethodView):
    """
    Product Adding Resource
    """
    @token_required
    def post(self, current_user):
        # get the post data
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            responseObject = {
                'status': 'fail',
                'message': 'You have 0 item in your cart.'
            }
            return make_response(jsonify(responseObject)), 202
        else:
            order = Order.query.filter_by(cart_id=cart.id).first()
            data = {
                'merchantId': BaseConfig.MERCHANT_ID,
                'amount': order.amount,
                'extraData': str(order.id)
            }
            order.update_status("PROCESSED")
            db.session.commit()

            hash_key='d46fbf37-5502-4e83-9b8c-ddd7427c9d88'
            signature = hmac.new(hash_key.encode('utf-8'), json.dumps(data, sort_keys=True).encode('utf-8'), md5).hexdigest()
            data['signature'] = signature

            auth_token = encode_merchant_token(data["merchantId"], data['signature'])

            headers={
                'x-access-token': auth_token
            }
            r = requests.post("http://localhost:8000/transaction/create", headers=headers, data=data)

            print(r.json())
            if 'data' not in r.json() or r.json()['data']['signature'] != signature:
                responseObject = {
                    'status': 'fail',
                    'message': 'Security alert!'
                }
                return make_response(jsonify(responseObject)), 400
            responseObject = {
                'status': 'success',
                'data': data
            }
            return make_response(jsonify(responseObject)), 201
        