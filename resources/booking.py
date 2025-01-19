from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_babel import _  

from db import db
from models import BookingModel
from schemas import BookingSchema

blp = Blueprint("Bookings", "bookings", description="Operations on bookings")

@blp.route("/booking")
class BookingList(MethodView):
    @blp.response(200, BookingSchema(many=True))
    def get(self):
        """Get a list of all bookings"""
        try:
            return BookingModel.query.all()
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching the bookings.")

    @blp.arguments(BookingSchema)
    @blp.response(201, BookingSchema)
    def post(self, booking_data):
        """Create a new booking and return the created booking with its ID"""
        booking = BookingModel(**booking_data)
        try:
            db.session.add(booking)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="A booking with that information already exists.")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred creating the booking.")
        return booking

@blp.route("/booking/<string:booking_id>")
class Booking(MethodView):
    @blp.response(200, BookingSchema)
    def get(self, booking_id):
        """Get a booking by ID"""
        try:
            return BookingModel.query.get_or_404(booking_id)
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching the booking.")

    @blp.arguments(BookingSchema)
    @blp.response(200, BookingSchema)
    def put(self, booking_data, booking_id):
        """Update a booking by ID (Replace all attributes except ID)"""
        booking = BookingModel.query.get_or_404(booking_id)
        try:
            booking.booking_date = booking_data["booking_date"]
            booking.booking_status = booking_data["booking_status"]
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while updating the booking.")
        return booking
    
    @blp.arguments(BookingSchema)
    @blp.response(200, BookingSchema)
    def patch(self, booking_data, booking_id):
        """Partially update a booking by ID"""
        booking = BookingModel.query.get_or_404(booking_id)
        try:
            if "booking_date" in booking_data:
                booking.booking_date = booking_data["booking_date"]
            if "booking_status" in booking_data:
                booking.booking_status = booking_data["booking_status"]
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while partially updating the booking.")
        return booking

    def delete(self, booking_id):
        """Delete a booking by ID"""
        booking = BookingModel.query.get_or_404(booking_id)
        try:
            db.session.delete(booking)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while deleting the booking.")
        return {"message": "Booking deleted successfully."}, 200
