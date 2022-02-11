from distutils.command import config
from flask import request, make_response, jsonify
from flask.views import MethodView
import requests
from hashlib import md5
import json

from project.server.config import BaseConfig
from project.server.database import db
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
        post_data = request.get_json()
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
                'extraData': order.id.hex
            }
            order.update_status("PROCESSED")
            db.session.commit()
            signature = md5(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()
            data['signature'] = signature
            print(data)
            r = requests.post("http://localhost:8000/transaction/create", 
                data = data)
            responseObject = {
                'status': 'success',
            }
            return make_response(jsonify(responseObject)), 201
        