import math

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
