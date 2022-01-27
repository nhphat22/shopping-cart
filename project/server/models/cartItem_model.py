from project.server.database import db
from sqlalchemy import Integer


class Cart(db.Model):
    """ CartItem Model for storing products in cart """
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    productId = db.Column(db.ARRAY(Integer), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False) 

    def __init__(self, productId, price, quantity):
        self.productId = productId
        self.price = self.price 
        self.subtotal = self.price*quantity
