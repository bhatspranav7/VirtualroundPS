# backend/app/routes/expenses.py
from fastapi import APIRouter

router = APIRouter()

@router.post("/expenses")
def submit_expense(amount: float, category: str):
    return {"message": f"Expense submitted: {amount} for {category}"}

@router.get("/expenses")
def get_expenses():
    return [{"id": 1, "amount": 100, "category": "Food", "status": "Pending"}]
