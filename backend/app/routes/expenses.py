from fastapi import APIRouter
from pydantic import BaseModel
import sqlite3
from ..config import DATABASE_PATH
from datetime import date

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])

# Request body schema
class ExpenseCreate(BaseModel):
    employee_id: int
    amount: float
    description: str
    category: str = "General"   # default category
    currency: str = "USD"       # default currency
    expense_date: date = date.today()  # default today

# Get all expenses
@router.get("/")
def get_expenses():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, employee_id, amount, description, status FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "employee_id": row[1],
            "amount": row[2],
            "description": row[3],
            "status": row[4]
        }
        for row in rows
    ]

# Add a new expense
@router.post("/")
def create_expense(expense: ExpenseCreate):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO expenses 
           (employee_id, amount, description, category, currency, expense_date, status) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (
            expense.employee_id,
            expense.amount,
            expense.description,
            expense.category,
            expense.currency,
            expense.expense_date,
            "Pending"
        )
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return {
        "id": new_id,
        "employee_id": expense.employee_id,
        "amount": expense.amount,
        "description": expense.description,
        "category": expense.category,
        "currency": expense.currency,
        "expense_date": str(expense.expense_date),
        "status": "Pending"
    }
