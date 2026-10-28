from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import select, func

from app.extensions import db
from app.models import Expense

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/reports/total", methods=["GET"])
@jwt_required()
def get_reports_total():

    current_user_id = int(get_jwt_identity())

    total_statement = select(func.sum(Expense.amount)).where(Expense.user_id == current_user_id)

    total_spending = db.session.execute(total_statement).scalar_one_or_none()

    if total_spending is None:
        total_spending = 0

    return {
        "total_spending": total_spending
    }



@reports_bp.route("/reports/categories", methods=["GET"])
@jwt_required()
def get_reports_total_by_category():

    current_user_id = int(get_jwt_identity())

    total_by_category_statement = select(Expense.category, func.sum(Expense.amount)).group_by(Expense.category).where(Expense.user_id == current_user_id)

    total_by_category_spending = db.session.execute(total_by_category_statement).all()

    if not total_by_category_spending:
        return {
            "categories": []
        }

    list_by_category = []

    for categories in total_by_category_spending:
        category_data = {
            "category": categories[0],
            "total": categories[1]
        }
        list_by_category.append(category_data)
    

    return {
        "categories" : list_by_category
    }



@reports_bp.route("/reports/monthly", methods=["GET"])
@jwt_required()
def get_reports_monthly():

    current_user_id = int(get_jwt_identity())

    month_expression = func.strftime("%Y-%m", Expense.date)

    monthly_statement = (
        select(
            month_expression.label("month"),
            func.sum(Expense.amount).label("total")
        )
        .where(Expense.user_id == current_user_id)
        .group_by(month_expression)
        .order_by(month_expression)
    )

    results = db.session.execute(monthly_statement).all()

    monthly_spending = [
        {"month": row.month, "total": row.total}
        for row in results
    ]

    return {"monthly_spending": monthly_spending}