from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config["DATABASE"] = "expenses.db"

    from app.routes import expenses_bp
    app.register_blueprint(expenses_bp)

    return app


