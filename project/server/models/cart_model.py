from project.server.database import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class Cart(db.Model):
    """ Cart Model for storing cartItems and subtotal """
    __tablename__ = "carts"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    cart_items = db.relationship(
        "CartItem",
        lazy="subquery",
        backref=db.backref("cartitems", lazy=True),
        cascade="all, delete",
    )
    total = db.Column(db.Float, nullable=False)
    vat = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    def __init__(self, user_id):
        self.user_id = user_id
        self.subtotal = 0 
        self.vat = self.subtotal * 0.1
        self.total = self.subtotal + self.vat
    
    def update_cash(self, subtotal):
        self.subtotal = subtotal
        self.vat = self.subtotal * 0.1
        self.total = self.subtotal + self.vat
