from app.extensions import db

class Expense(db.Model):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    amount = db.Column(db.Float)
    category = db.Column(db.String)
    date = db.Column(db.String)
