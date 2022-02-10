from project.server.database import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class Order(db.Model):
    """  """
    __tablename__ = "orders"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    cart_id =  db.Column(UUID(as_uuid=True), db.ForeignKey('carts.id'), 
                            default=uuid4, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum("WAITING", "PROCESSED", "COMPLETE"   , 
                        name="order_status", create_type=False), nullable=False)

    def __init__(self, cart_id, amount):
        self.cart_id = cart_id
        self.amount = amount
        self.status = "WAITING"
    
    def update_status(self, status):
        self.status = status