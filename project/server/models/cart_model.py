from project.server.database import db
from sqlalchemy import Integer
from project.server.models.user_model import User

class Cart(db.Model):
    """ Cart Model for storing cartItems and subtotal """
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    cartItems = db.Column(db.ARRAY(Integer), nullable=False)
    total = db.Column(db.Float, nullable=False)
    vat = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    def __init__(self, cartItems):
        self.cartItems = cartItems
        self.total = sum(cartItems) #!!!!!
        self.vat = self.total * 0.1
        self.subtotal = self.total + self.vat