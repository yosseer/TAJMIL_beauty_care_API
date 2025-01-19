from db import db
from sqlalchemy.orm import relationship

class BookingModel(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    booking_status = db.Column(db.String(50), nullable=False, default="pending")

    # Relationships
    service = relationship('ServiceModel', back_populates='bookings', cascade="all, delete")
    user = relationship('UserModel', back_populates='bookings', cascade="all, delete")
