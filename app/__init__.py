from flask import Flask
from app.database import close_db_connection
from app.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig


def create_app(config=DevelopmentConfig):
    app = Flask(__name__)

    app.config.from_object(config)

    app.teardown_appcontext(close_db_connection)

    from app.routes import expenses_bp
    app.register_blueprint(expenses_bp)

    return app


