from flask import Blueprint, request
from datetime import datetime
from app.validation import validate_expense,allowed_categories
from app.extensions import db
from app.models import Expense
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


expenses_bp = Blueprint("expenses",__name__)



@expenses_bp.route("/expenses", methods=["GET"])
@jwt_required()
def get_expenses():

    current_user_id = int(get_jwt_identity())

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

    statement = db.select(Expense).where(Expense.user_id == current_user_id)

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
    



@expenses_bp.route("/expenses/<int:expense_id>", methods=["GET"])
@jwt_required()
def get_expense(expense_id):

    current_user_id = int(get_jwt_identity())

    statement = db.select(Expense).where(
        Expense.id == expense_id
    ).where(
        Expense.user_id == current_user_id
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
@jwt_required()
def create_expense():

    current_user_id = int(get_jwt_identity())

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
        date=date,
        user_id=current_user_id
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
@jwt_required()
def update_expense(expense_id):

    current_user_id = int(get_jwt_identity())

    data = request.get_json(silent=True)

    error = validate_expense(data)

    if error is not None:
        return error, 400

    name = data["name"]
    amount = data["amount"]
    category = data["category"]

    statement = db.select(Expense).where(
        Expense.id == expense_id
    ).where(
        Expense.user_id == current_user_id
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
@jwt_required()
def delete_expense(expense_id):

    current_user_id = int(get_jwt_identity())

    statement = db.select(Expense).where(
        Expense.id == expense_id
    ).where(
        Expense.user_id == current_user_id
    )

    expense = db.session.execute(statement).scalar_one_or_none()

    if expense is None:
        return {"error": "Expense not found"}, 404

    db.session.delete(expense)

    db.session.commit()

    return {"message": "Expense deleted successfully"}, 200







@expenses_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json(silent=True)

    if data is None:
        return {"error": "User Name and Password is required"}, 400

    if "user_name" not in data:
        return {"error": "User Name is required"}, 400

    if "password" not in data:
        return {"error": "Password is required"}, 400

    user_name = data["user_name"]
    password = data["password"]

    statement = db.select(User).where(User.user_name == user_name)
    user_exists = db.session.execute(statement).scalar_one_or_none()

    if user_exists is not None:
        return {"error": "user_name already exists"}, 400

    password_hash = generate_password_hash(password)

    user = User(
        user_name = user_name,
        password_hash = password_hash
    )

    db.session.add(user)
    db.session.commit()

    return {"message": "User is registered"}, 201



@expenses_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json(silent=True)

    if data is None:
        return {"error": "Credentials are required"}, 400

    if "user_name" not in data:
        return {"error": "user_name is required"}, 400

    if "password" not in data:
        return {"error": "password is required"}, 400

    user_name = data["user_name"]
    password = data["password"]

    statement = db.select(User).where(User.user_name == user_name)
    user_exists = db.session.execute(statement).scalar_one_or_none()

    if user_exists is None:
        return {"error": "Invalid Credentials"}, 401

    stored_password_hash = user_exists.password_hash

    if not check_password_hash(stored_password_hash, password):
        return {"error": "Invalid Credentials"}, 401

    access_token = create_access_token(identity=str(user_exists.id))

    return {
        "message": "Login successful",
        "access_token": access_token
    }, 200


@expenses_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()

    return {
        "user_id": user_id
    }, 200