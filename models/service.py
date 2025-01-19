from db import db
from sqlalchemy.orm import relationship

class ServiceModel(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False, unique=True, index=True)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False, default=0.0)

    # One-to-Many Relationship
    bookings = relationship("BookingModel", back_populates="service", lazy="select", cascade="all, delete")
