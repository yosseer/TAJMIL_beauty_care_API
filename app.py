from flask import Flask, request
from flask_smorest import Api
from flask_babel import Babel
from db import db
from resources.__init__ import *

def create_app():
    app = Flask(__name__)

    # Application Configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["API_TITLE"] = "TAJMIL Beauty & Care API"
    app.config["API_VERSION"] = "1.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["BABEL_DEFAULT_LOCALE"] = "en"
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations" 

    # Initialize Extensions
    db.init_app(app)
    api = Api(app)
    babel = Babel(app)

    # Locale Selector
    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(["ar", "fr", "en"])
    
    # Register Blueprints
    try:
        api.register_blueprint(UserBlueprint)
        api.register_blueprint(ProductBlueprint)
        api.register_blueprint(ServiceBlueprint)
        api.register_blueprint(BookingBlueprint)
    except Exception as e:
        app.logger.error(f"Error registering blueprints: {e}")

    # Create database tables
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
