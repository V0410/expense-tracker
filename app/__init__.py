from flask import Flask
from app.database import close_db_connection


def create_app():
    app = Flask(__name__)

    app.config["DATABASE"] = "expenses.db"

    app.teardown_appcontext(close_db_connection)

    from app.routes import expenses_bp
    app.register_blueprint(expenses_bp)

    return app


