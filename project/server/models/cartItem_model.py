from project.server.database import db


class CartItem(db.Model):
    """ CartItem Model for storing products in cart """
    __tablename__ = "cartitems"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_id =  db.Column(db.Integer, db.ForeignKey('carts.id'),
        nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False) 

    def __init__(self, cart_id, product_id, price, quantity):
        self.cart_id = cart_id
        self.product_id = product_id
        self.price = price 
        self.quantity = quantity
        self.subtotal = price * quantity 
    
    def update_quantity(self, quantity):
        self.quantity += quantity
        self.subtotal = self.price * quantity
