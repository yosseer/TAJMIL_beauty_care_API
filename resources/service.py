from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_babel import _  

from db import db
from models import ServiceModel
from schemas import ServiceSchema

blp = Blueprint("Services", "services", description="Operations on services")

@blp.route("/service")
class ServiceList(MethodView):
    @blp.response(200, ServiceSchema(many=True))
    def get(self):
        """Get a list of all services"""
        try:
            return ServiceModel.query.all()
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching the services.")

    @blp.arguments(ServiceSchema)
    @blp.response(201, ServiceSchema)
    def post(self, service_data):
        """Create a new service and return the created service with its ID"""
        service = ServiceModel(**service_data)
        try:
            db.session.add(service)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="A service with that name already exists.")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred creating the service.")
        return service

@blp.route("/service/<string:service_id>")
class Service(MethodView):
    @blp.response(200, ServiceSchema)
    def get(self, service_id):
        """Get a service by ID"""
        try:
            return ServiceModel.query.get_or_404(service_id)
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching the service.")

    @blp.arguments(ServiceSchema)
    @blp.response(200, ServiceSchema)
    def put(self, service_data, service_id):
        """Update a service by ID"""
        service = ServiceModel.query.get_or_404(service_id)
        if not service:
            abort(404, message=f"Service with ID {service_id} not found.")
        try:
            service.name = service_data["name"]
            service.description = service_data["description"]
            service.price = service_data["price"]
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while updating the service.")
        return service

    @blp.arguments(ServiceSchema)
    @blp.response(200, ServiceSchema)
    def patch(self, service_data, service_id):
        """Partially update a service by ID"""
        service = ServiceModel.query.get_or_404(service_id)
        if not service:
            abort(404, message=f"Service with ID {service_id} not found.")
        try:
            if "name" in service_data:
                service.name = service_data["name"]
            if "description" in service_data:
                service.description = service_data["description"]
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while partially updating the service.")
        return service

    def delete(self, service_id):
        """Delete a service by ID"""
        service = ServiceModel.query.get_or_404(service_id)
        try:
            db.session.delete(service)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while deleting the service.")
        return {"message": "Service deleted successfully."}, 200
