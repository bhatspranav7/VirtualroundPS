# backend/app/routes/approvals.py
from fastapi import APIRouter

router = APIRouter()

@router.post("/approve/{expense_id}")
def approve(expense_id: int):
    return {"message": f"Expense {expense_id} approved"}

@router.post("/reject/{expense_id}")
def reject(expense_id: int):
    return {"message": f"Expense {expense_id} rejected"}
