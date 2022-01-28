from flask import request, make_response, jsonify
from flask.views import MethodView

from project.server.database import db
from project.server.models.product_model import Product

#admin
class AddProductAPI(MethodView):
    """
    Product Adding Resource
    """
    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if product already exists
        product = Product.query.filter_by(name=post_data.get('name')).first()
        if not product:
            try:
                product = Product(
                    name=post_data.get('name'),
                    price=post_data.get('price')
                )
                # insert the user
                db.session.add(product)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully adding new product.',
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Product already exists. Please Add another.',
            }
            return make_response(jsonify(responseObject)), 202