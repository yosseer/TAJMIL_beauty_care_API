from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_babel import _  

from db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/user")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        """Get a list of all users"""
        try:
            return UserModel.query.all()
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching the users.")

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        """Create a new user and return the created user with its ID"""
        user = UserModel(**user_data)
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="A user with that username already exists.")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred creating the user.")
        return user

@blp.route("/user/<string:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        """Get a user by ID"""
        try:
            return UserModel.query.get_or_404(user_id)
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching the user.")

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def put(self, user_data, user_id):
        """Update a user by ID"""
        user = UserModel.query.get_or_404(user_id)
        if not user:
            abort(404, message=f"User with ID {user_id} not found.")
        try:
            user.username = user_data["username"]
            user.email = user_data["email"]
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while updating the user.")
        return user

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def patch(self, user_data, user_id):
        """Partially update a user by ID"""
        user = UserModel.query.get_or_404(user_id)
        if not user:
            abort(404, message=f"User with ID {user_id} not found.")
        try:
            if "username" in user_data:
                user.username = user_data["username"]
            if "email" in user_data:
                user.email = user_data["email"]
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while partially updating the user.")
        return user
    
    def delete(self, user_id):
        """Delete a user by ID"""
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while deleting the user.")
        return {"message": "User deleted successfully."}, 200
