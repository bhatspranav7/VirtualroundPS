"""
Main FastAPI application entry point for the Expense Approval System.
Initializes FastAPI, configures middleware, and includes routers.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Import routers
from .routes import auth, users, expenses, approvals
from .config import DATABASE_PATH, DATABASE_URL, SECRET_KEY, DEBUG
import os

# Database initialization functions
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
            role TEXT NOT NULL CHECK(role IN ('Admin', 'Manager', 'Employee')),
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
            status TEXT NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending', 'Approved', 'Rejected', 'In Review')),
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
            status TEXT NOT NULL DEFAULT 'Pending' CHECK(status IN ('Pending', 'Approved', 'Rejected')),
            comments TEXT,
            approved_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (expense_id) REFERENCES expenses(id),
            FOREIGN KEY (approver_id) REFERENCES users(id)
        )
    """)

    # Approval rules table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS approval_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_name TEXT NOT NULL,
            rule_type TEXT NOT NULL CHECK(rule_type IN ('amount_threshold', 'percentage_approval', 'specific_approver', 'department_rule')),
            condition_value REAL,
            approver_role TEXT,
            approver_id INTEGER,
            approval_level INTEGER NOT NULL,
            department TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (approver_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    insert_sample_data(cursor)
    conn.commit()
    conn.close()


def insert_sample_data(cursor):
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
    hashed_password = pwd_context.hash("password123")


    # Insert sample users
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        return  # Already inserted

    users_data = [
        (1, "admin@company.com", hashed_password, "Alice Admin", "Admin", None, "Management"),
        (2, "manager@company.com", hashed_password, "Bob Manager", "Manager", 1, "Engineering"),
        (3, "employee@company.com", hashed_password, "Charlie Employee", "Employee", 2, "Engineering"),
    ]
    cursor.executemany("""
        INSERT INTO users (id, email, hashed_password, full_name, role, manager_id, department)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, users_data)

    # Sample approval rules
    approval_rules_data = [
        ("Under $100 - Manager Approval", "amount_threshold", 100.0, "Manager", None, 1, None),
        ("$100-$1000 - Manager & Admin", "amount_threshold", 1000.0, "Manager", None, 1, None),
        ("Over $1000 - Multi-level", "amount_threshold", 1000.0, "Admin", None, 2, None),
        ("Travel Expenses - Special Approver", "specific_approver", None, None, 2, 1, None),
    ]
    cursor.executemany("""
        INSERT INTO approval_rules (rule_name, rule_type, condition_value, approver_role, approver_id, approval_level, department)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, approval_rules_data)

    # Sample expenses
    expenses_data = [
        (3, 45.50, "USD", "Office Supplies", "Printer paper and pens", "2025-10-01", None, "Pending"),
        (3, 350.00, "USD", "Software", "Adobe Creative Cloud subscription", "2025-10-02", None, "Pending"),
        (3, 1500.00, "USD", "Travel", "Flight to client meeting", "2025-10-03", None, "Pending"),
    ]
    cursor.executemany("""
        INSERT INTO expenses (employee_id, amount, currency, category, description, expense_date, receipt_url, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, expenses_data)

    print("✓ Sample data inserted successfully")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Expense Approval System...")
    init_database()
    print("✓ Database initialized")
    yield
    print("👋 Shutting down Expense Approval System...")


# Initialize FastAPI
app = FastAPI(
    title="Expense Approval System",
    description="Multi-level expense approval system with workflow engine",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Expense Approval System"}

@app.get("/api/expenses/")
def get_expenses():
    # Add logic here to retrieve and return a list of expenses
    # For example, you might fetch data from your database.
    return {"message": "Endpoint for getting expenses is now working"}

@app.get("/api/approvals/")
def get_approvals():
    # Add logic here to retrieve and return a list of approvals
    return {"message": "Endpoint for getting approvals is now working"}

@app.post("/")
def handle_post_root(data: dict):
    # Handle the POST request data here
    return {"received": data}

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/api/auth/login")
def login(credentials: dict):
    # Add logic here to validate user credentials
    # and return an authentication token or a success message.
    return {"message": "Login endpoint is now configured to accept POST requests"}

# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "type": type(exc).__name__}
    )

# Health check endpoints
@app.get("/", tags=["Health"])
async def root():
    return {"message": "Expense Approval System API", "status": "running", "version": "1.0.0", "docs": "/docs"}

@app.get("/health", tags=["Health"])
async def health_check():
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        conn.close()
        return {"status": "healthy", "database": "connected", "users_count": user_count}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(expenses.router, prefix="/api/expenses", tags=["Expenses"])
app.include_router(approvals.router, prefix="/api/approvals", tags=["Approvals"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
