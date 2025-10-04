"""
Main FastAPI application for Expense Reimbursement System.
Includes routers for authentication, users, expenses, and approvals.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from contextlib import asynccontextmanager
import os

# ---------------- CONFIG ----------------
DATABASE_PATH = "expense_system.db"

# ---------------- DATABASE INIT ----------------
def init_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Admin','Manager','Employee')),
            manager_id INTEGER,
            department TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            FOREIGN KEY (manager_id) REFERENCES users(id)
        )
    """)

    # Expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            currency TEXT NOT NULL DEFAULT 'USD',
            category TEXT NOT NULL,
            description TEXT,
            expense_date DATE NOT NULL,
            receipt_url TEXT,
            status TEXT NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending','Approved','Rejected','In Review')),
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES users(id)
        )
    """)

    # Approvals table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS approvals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_id INTEGER NOT NULL,
            approver_id INTEGER NOT NULL,
            approval_level INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending','Approved','Rejected')),
            comments TEXT,
            approved_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (expense_id) REFERENCES expenses(id),
            FOREIGN KEY (approver_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

# ---------------- FASTAPI LIFESPAN ----------------

# Initialize database at app startup
if not os.path.exists(DATABASE_PATH):
    init_database()
    print("✓ Database initialized with tables")



# ---------------- FASTAPI APP ----------------
app = FastAPI(
    title="Expense Approval System",
    version="1.0.0",
    description="Multi-level expense approval system"
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Expense Approval System API", "status": "running", "docs": "/docs"}

# Health check
@app.get("/health")
def health_check():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        conn.close()
        return {"status": "healthy", "database": "connected", "users_count": user_count}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


# ---------------- IMPORT ROUTERS ----------------
from app.routes import auth, users, expenses, approvals

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(expenses.router)
app.include_router(approvals.router)


# ---------------- RUN ----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
