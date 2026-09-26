from flask import Flask
from app.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig
from app.extensions import db, migrate, jwt


def create_app(config=DevelopmentConfig, db_path=None):
    app = Flask(__name__)

    app.config.from_object(config)

    if db_path:
        app.config["DATABASE"] = str(db_path)
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + app.config["DATABASE"]


    db.init_app(app)

    migrate.init_app(app, db)

    jwt.init_app(app)

    from app.routes import expenses_bp
    app.register_blueprint(expenses_bp)

    return app


