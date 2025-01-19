from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_babel import _  

from db import db
from models import ProductModel
from schemas import ProductSchema

blp = Blueprint("Products", "products", description="Operations on products")

@blp.route("/product")
class ProductList(MethodView):
    @blp.response(200, ProductSchema(many=True))
    def get(self):
        """Get a list of all products"""
        try:
            return ProductModel.query.all()
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching the products.")

    @blp.arguments(ProductSchema)
    @blp.response(201, ProductSchema)
    def post(self, product_data):
        """Create a new product and return the created product with its ID"""
        product = ProductModel(**product_data)
        try:
            db.session.add(product)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            abort(400, message="A product with that name already exists.")
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred creating the product.")
        return product

@blp.route("/product/<string:product_id>")
class Product(MethodView):
    @blp.response(200, ProductSchema)
    def get(self, product_id):
        """Get a product by ID"""
        try:
            return ProductModel.query.get_or_404(product_id)
        except SQLAlchemyError:
            abort(500, message="An error occurred while fetching the product.")

    @blp.arguments(ProductSchema)
    @blp.response(200, ProductSchema)
    def put(self, product_data, product_id):
        """Update a product by ID"""
        product = ProductModel.query.get_or_404(product_id)
        if not product:
            abort(404, message=f"Product with ID {product_id} not found.")
        try:
            product.name = product_data["name"]
            product.price = product_data["price"]
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while updating the product.")
        return product

    @blp.arguments(ProductSchema)
    @blp.response(200, ProductSchema)
    def patch(self, product_data, product_id):
        """Partially update a product by ID"""
        product = ProductModel.query.get_or_404(product_id)
        if not product:
            abort(404, message=f"Product with ID {product_id} not found.")
        try:
            if "name" in product_data:
                product.name = product_data["name"]
            if "price" in product_data:
                product.price = product_data["price"]
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while partially updating the product.")
        return product

    def delete(self, product_id):
        """Delete a product by ID"""
        product = ProductModel.query.get_or_404(product_id)
        try:
            db.session.delete(product)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message="An error occurred while deleting the product.")
        return {"message": "Product deleted successfully."}, 200
