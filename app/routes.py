from flask import Blueprint, request
from datetime import datetime
from app.validation import validate_expense,allowed_categories, validate_user
from app.extensions import db
from app.models import Expense
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import current_app
from sqlalchemy import func, select
import math


expenses_bp = Blueprint("expenses",__name__)



@expenses_bp.route("/expenses", methods=["GET"])
@jwt_required()
def get_expenses():

    current_user_id = int(get_jwt_identity())

    category = request.args.get("category")
    min_amount = request.args.get("min_amount")
    month = request.args.get("month")
    page = (request.args.get("page"))
    per_page = (request.args.get("per_page"))

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

    if page is None:
        page = 1
    else:
        try:
            page = int(page)
        except ValueError:
            return {"error": "Page must be an integer"}, 400

    if per_page is None:
        per_page = 10
    else:
        try:
            per_page = int(per_page)
        except ValueError:
            return {"error": "Per_page must be an integer"}, 400

    if page < 1:
        return {"error": "Invalid Page number"}, 400

    if per_page < 1 or per_page > 100:
        return {"error": "Invalid per_page number"}, 400

    # statement = db.select(Expense).where(Expense.user_id == current_user_id)

    conditions = [Expense.user_id == current_user_id]

    if category:
        conditions.append(Expense.category == category)

    if min_amount is not None:
        conditions.append(Expense.amount >= min_amount)

    if month:
        conditions.append(Expense.date.like(f"{month}%"))

    statement = (
        select(Expense)
        .where(*conditions)
        .order_by(Expense.id)
        )

    total_statement = select(func.count(Expense.id)).where(*conditions)

    total_expenses = db.session.execute(total_statement).scalar()

    total_pages = math.ceil(total_expenses / per_page)

    offset = (page - 1) * per_page

    statement = statement.limit(per_page).offset(offset)

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


    # return expenses_dict, 200

    return {
        "expenses": expenses_dict,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total_expenses,
            "pages": total_pages
        }
    }, 200
    



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
    
    name = data["name"].strip()
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

    error = validate_user(data)

    if error is not None:
        return error, 400
    
    user_name = data["user_name"].strip()
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

    error = validate_user(data)

    if error is not None:
        return error, 400

    user_name = data["user_name"].strip()
    password = data["password"]

    statement = db.select(User).where(User.user_name == user_name)
    user_exists = db.session.execute(statement).scalar_one_or_none()

    if user_exists is None:
        current_app.logger.warning(f"Failed login attempt for unknown user '{user_name}'")
        return {"error": "Invalid Credentials"}, 401

    stored_password_hash = user_exists.password_hash

    if not check_password_hash(stored_password_hash, password):
        current_app.logger.warning(f"Failed login attempt for user '{user_name}'")
        return {"error": "Invalid Credentials"}, 401

    access_token = create_access_token(identity=str(user_exists.id))

    current_app.logger.info(f"User '{user_name}' logged in successfully")

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