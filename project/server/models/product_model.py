from project.server.database import db
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class Product(db.Model):
    """ Product Model for storing product related details """
    __tablename__ = "products"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price