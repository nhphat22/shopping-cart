from project.server.database import db


class CartItem(db.Model):
    """ CartItem Model for storing products in cart """
    __tablename__ = "cartitems"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False) 

    def __init__(self, product_id, price, quantity):
        self.product_id = product_id
        self.price = price 
        self.quantity = quantity
        self.subtotal = price * quantity 
