from flask import Blueprint, request
from datetime import datetime
from app.validation import validate_expense,allowed_categories
from app.extensions import db
from app.models import Expense

expenses_bp = Blueprint("expenses",__name__)



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

    statement = db.select(Expense)

    if category:
        statement = statement.where(
            Expense.category == category
        )

    if min_amount is not None:
        statement = statement.where(
            Expense.amount >= min_amount
        )

    if month:
        statement = statement.where(
            Expense.date.like(f"{month}%")
        )

    expenses = db.session.execute(statement).scalars().all()

    expenses_dict = []
    for expense in expenses:
        expenses_dict.append({
            "id": expense.id,
            "name": expense.name,
            "amount": expense.amount,
            "category": expense.category,
            "date": expense.date
        })

    return expenses_dict, 200
    



@expenses_bp.route("/expenses/<int:expense_id>")
def get_expense(expense_id):

    statement = db.select(Expense).where(
        Expense.id == expense_id
    )
    expense = db.session.execute(statement).scalar_one_or_none()

    if expense is None:
        return {"error": "Expense not found"}, 404

    return {
        "id": expense.id,
        "name": expense.name,
        "amount": expense.amount,
        "category": expense.category,
        "date": expense.date
    }, 200



    
@expenses_bp.route("/expenses", methods=["POST"])
def create_expense():
    data = request.get_json(silent=True)

    error = validate_expense(data)

    if error is not None:
        return error, 400
    
    name = data["name"]
    amount = data["amount"]
    category = data["category"]
    date = datetime.now().strftime("%Y-%m-%d")

    expense = Expense(
        name=name,
        amount=amount,
        category=category,
        date=date
    )

    db.session.add(expense)

    db.session.commit()

    return {
        "message": "Expense Created",
        "expense": {
            "id": expense.id,
            "name": expense.name,
            "amount": expense.amount,
            "category": expense.category,
            "date": expense.date
        }
    }, 201



@expenses_bp.route("/expenses/<int:expense_id>", methods=["PUT"])
def update_expense(expense_id):
    data = request.get_json(silent=True)

    error = validate_expense(data)

    if error is not None:
        return error, 400

    name = data["name"]
    amount = data["amount"]
    category = data["category"]

    statement = db.select(Expense).where(
        Expense.id == expense_id
    )

    expense = db.session.execute(statement).scalar_one_or_none()

    if expense is None:
        return {"error": "Expense not found"}, 404

    expense.name = name
    expense.amount = amount
    expense.category = category

    db.session.commit()

    return {
        "message": "Expense updated successfully",
        "expense":{
            "id": expense.id,
            "name": expense.name,
            "amount": expense.amount,
            "category": expense.category,
            "date": expense.date
        }
    }, 200



@expenses_bp.route("/expenses/<int:expense_id>", methods=["DELETE"])
def delete_expense(expense_id):

    statement = db.select(Expense).where(
        Expense.id == expense_id
    )

    expense = db.session.execute(statement).scalar_one_or_none()

    if expense is None:
        return {"error": "Expense not found"}, 404

    db.session.delete(expense)

    db.session.commit()

    return {"message": "Expense deleted successfully"}, 200

    

