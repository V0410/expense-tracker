from flask import Blueprint, request
from app.database import get_db_connection
from datetime import datetime

expenses_bp = Blueprint("expenses",__name__)


allowed_categories = ["food", "transport", "shopping", "bills", "other"]


@expenses_bp.route("/expenses")
def get_expenses():
    category = request.args.get("category")
    min_amount = request.args.get("min_amount")
    month = request.args.get("month")

    if category and category not in allowed_categories:
        return {"error": "Invalid Category"}, 400

    if min_amount is not None:
        try:
            min_amount = float(min_amount)
        except ValueError:
            return {"error": "Invalid minimum amount"}, 400

        if min_amount < 0:
            return {"error": "Minimum amount must be greater than Zero"}, 400

    if month is not None:
        try:
            datetime.strptime(month, "%Y-%m")
        except ValueError:
            return {"error": "Invalid Month Format. Use YYYY-MM"}, 400


    query = "SELECT * FROM expenses"
    conditions = []
    parameters = []

    if category:
        conditions.append("category=?")
        parameters.append(category)

    if min_amount is not None:
        conditions.append("amount >= ?")
        parameters.append(min_amount)

    if month is not None:
        conditions.append("date LIKE ?")
        parameters.append(f"{month}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)


    connection = get_db_connection()

    expenses = connection.execute(query, parameters).fetchall()

    connection.close()

    return [dict(expense) for expense in expenses], 200

