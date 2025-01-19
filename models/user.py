from db import db
from sqlalchemy.orm import relationship

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password = db.Column(db.String(128), nullable=False)

    # One-to-Many Relationship
    bookings = relationship("BookingModel", back_populates="user", lazy="select", cascade="all, delete")
