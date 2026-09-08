from flask import Blueprint, request
from app.database import get_db_connection
from datetime import datetime
import math

expenses_bp = Blueprint("expenses",__name__)


allowed_categories = ["food", "transport", "shopping", "bills", "other"]

def validate_expense(data):
    if data is None:
        return {"error": "Request body must contain JSON object"}

    if not isinstance(data, dict):
        return {"error": "Request body must be a JSON object"}

    if "name" not in data:
        return {"error": "Name is required"}

    if "amount" not in data:
        return {"error": "Amount is required"}

    if "category" not in data:
        return {"error": "Category is required"}

    if not isinstance(data["name"], str):
        return {"error": "Name must be a string"}

    if (
        not isinstance(data["amount"], (int, float)) or isinstance(data["amount"], bool)
    ):
        return {"error": "Amount must be a number"}

    if not math.isfinite(data["amount"]):
        return {"error": "Amount must be a finite number"}

    if not isinstance(data["category"], str):
        return {"error": "Category must be a string"}
    
    if not data["name"].strip():
        return {"error": "Name can't be empty"}

    if data["amount"] <= 0:
        return {"error": "Amount must be greater than Zero"}

    if data["category"] not in allowed_categories:
        return {"error": "Invalid Category"}

    return None



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



@expenses_bp.route("/expenses/<int:expense_id>")
def get_expense(expense_id):
    connection = get_db_connection()

    expense = connection.execute("SELECT * FROM expenses WHERE id = ?",(expense_id,)).fetchone()

    connection.close()

    if expense is None:
        return {"error": "Expense not found"}, 404

    return dict(expense), 200



@expenses_bp.route("/expenses", methods=["POST"])
def create_expense():
    data = request.get_json(silent=True)

    error = validate_expense(data)

    if data is not None:
        return error, 400
    
    name = data["name"]
    amount = data["amount"]
    category = data["category"]
    date = datetime.now().strftime("%Y-%m-%d")

    connection = get_db_connection()

    cursor = connection.execute("""
        INSERT INTO expenses
        (name, amount, category, date)
        VALUES
        (?, ?, ?, ?)
    """,(name, amount, category, date))

    connection.commit()

    expense_id = cursor.lastrowid

    expense = connection.execute("SELECT * FROM expenses WHERE id = ?",(expense_id, )).fetchone()

    connection.close()

    return {
        "message": "Expense Created",
        "expense": dict(expense)
    }, 201



@expenses_bp.route("/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    data = request.get_json(silent=True)

    error = validate_expense(data)

    if error is not None:
        return error, 400

    connection = get_db_connection()

    expense = connection.execute("SELECT * FROM expenses WHERE id = ?",(expense_id,)).fetchone()

    if expense is None:
        connection.close()
        return {"error": "Expense not found"}, 404

    name = data["name"]
    amount = data["amount"]
    category = data["category"]

    connection.execute("""UPDATE expenses
        SET name = ?, amount = ?, category = ?
        WHERE id = ?
    """,(name, amount, category, expense_id))

    connection.commit()

    updated_expense = connection.execute("SELECT * FROM expenses WHERE id = ?",(expense_id,)).fetchone()

    connection.close()

    return {
        "message": "Expense updated successfully",
        "Expense": dict(updated_expense)
    }, 200


@expenses_bp.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):
    connection = get_db_connection()

    cursor = connection.execute("""
        DELETE FROM expenses WHERE id = ?
    """,(expense_id,))

    connection.commit()

    if cursor.rowcount == 0:
        connection.close()
        return {"error": "Expense not found"}, 404

    connection.close()

    return {"message": "Expense deleted successfully"}, 200

