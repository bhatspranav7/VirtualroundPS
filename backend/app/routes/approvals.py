from fastapi import APIRouter, HTTPException
import sqlite3
from ..config import DATABASE_PATH

router = APIRouter(prefix="/approvals", tags=["Approvals"])

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/pending")
def get_pending_requests():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE status = 'Pending'")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.put("/{expense_id}/approve")
def approve_request(expense_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    expense = cursor.fetchone()
    if expense is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Expense not found")
    cursor.execute(
        "UPDATE expenses SET status = 'Approved', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (expense_id,)
    )
    conn.commit()
    conn.close()
    return {"message": f"Expense {expense_id} approved successfully."}

@router.put("/{expense_id}/reject")
def reject_request(expense_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    expense = cursor.fetchone()
    if expense is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Expense not found")
    cursor.execute(
        "UPDATE expenses SET status = 'Rejected', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (expense_id,)
    )
    conn.commit()
    conn.close()
    return {"message": f"Expense {expense_id} rejected successfully."}
