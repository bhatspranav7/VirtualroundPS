"""
Database models and helper functions for the Expense Approval System.
This file contains database connection utilities and data access functions.
"""

import sqlite3
from typing import Optional, List, Dict, Any
from datetime import datetime
from contextlib import contextmanager

DATABASE_PATH = "expenses.db"


@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    Automatically handles connection closing and provides row factory for dict-like access.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    try:
        yield conn
    finally:
        conn.close()


def dict_from_row(row: sqlite3.Row) -> Dict[str, Any]:
    """
    Convert sqlite3.Row object to a dictionary.
    """
    return dict(zip(row.keys(), row))


# ==================== USER MODEL ====================

class UserModel:
    """
    User model for database operations.
    Handles CRUD operations for users table.
    """
    
    @staticmethod
    def create_user(email: str, hashed_password: str, full_name: str, 
                   role: str, manager_id: Optional[int] = None, 
                   department: Optional[str] = None) -> int:
        """
        Create a new user in the database.
        Returns the created user's ID.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (email, hashed_password, full_name, role, manager_id, department)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (email, hashed_password, full_name, role, manager_id, department))
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user by email address.
        Returns user data as a dictionary or None if not found.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ? AND is_active = 1", (email,))
            row = cursor.fetchone()
            return dict_from_row(row) if row else None
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve a user by ID.
        Returns user data as a dictionary or None if not found.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ? AND is_active = 1", (user_id,))
            row = cursor.fetchone()
            return dict_from_row(row) if row else None
    
    @staticmethod
    def get_all_users(role: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all active users, optionally filtered by role.
        Returns a list of user dictionaries.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if role:
                cursor.execute("SELECT * FROM users WHERE role = ? AND is_active = 1", (role,))
            else:
                cursor.execute("SELECT * FROM users WHERE is_active = 1")
            rows = cursor.fetchall()
            return [dict_from_row(row) for row in rows]
    
    @staticmethod
    def update_user(user_id: int, **kwargs) -> bool:
        """
        Update user fields dynamically.
        Returns True if successful, False otherwise.
        """
        if not kwargs:
            return False
        
        # Build dynamic UPDATE query
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [user_id]
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE users SET {set_clause} WHERE id = ?", values)
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        """
        Soft delete a user by setting is_active to 0.
        Returns True if successful, False otherwise.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET is_active = 0 WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def get_users_by_role(role: str) -> List[Dict[str, Any]]:
        """
        Get all users with a specific role.
        Useful for finding all managers or admins.
        """
        return UserModel.get_all_users(role=role)


# ==================== EXPENSE MODEL ====================

class ExpenseModel:
    """
    Expense model for database operations.
    Handles CRUD operations for expenses table.
    """
    
    @staticmethod
    def create_expense(employee_id: int, amount: float, currency: str,
                      category: str, description: str, expense_date: str,
                      receipt_url: Optional[str] = None) -> int:
        """
        Create a new expense in the database.
        Returns the created expense's ID.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO expenses (employee_id, amount, currency, category, description, 
                                    expense_date, receipt_url, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending')
            """, (employee_id, amount, currency, category, description, expense_date, receipt_url))
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def get_expense_by_id(expense_id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieve an expense by ID with employee details.
        Returns expense data with joined user information.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.*, u.full_name as employee_name, u.email as employee_email, 
                       u.department as employee_department
                FROM expenses e
                JOIN users u ON e.employee_id = u.id
                WHERE e.id = ?
            """, (expense_id,))
            row = cursor.fetchone()
            return dict_from_row(row) if row else None
    
    @staticmethod
    def get_expenses_by_employee(employee_id: int, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve all expenses for a specific employee.
        Optionally filter by status (Pending, Approved, Rejected, In Review).
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute("""
                    SELECT e.*, u.full_name as employee_name, u.email as employee_email
                    FROM expenses e
                    JOIN users u ON e.employee_id = u.id
                    WHERE e.employee_id = ? AND e.status = ?
                    ORDER BY e.submitted_at DESC
                """, (employee_id, status))
            else:
                cursor.execute("""
                    SELECT e.*, u.full_name as employee_name, u.email as employee_email
                    FROM expenses e
                    JOIN users u ON e.employee_id = u.id
                    WHERE e.employee_id = ?
                    ORDER BY e.submitted_at DESC
                """, (employee_id,))
            rows = cursor.fetchall()
            return [dict_from_row(row) for row in rows]
    
    @staticmethod
    def get_all_expenses(status: Optional[str] = None, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Retrieve all expenses with employee details.
        Optionally filter by status and limit results.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute("""
                    SELECT e.*, u.full_name as employee_name, u.email as employee_email,
                           u.department as employee_department
                    FROM expenses e
                    JOIN users u ON e.employee_id = u.id
                    WHERE e.status = ?
                    ORDER BY e.submitted_at DESC
                    LIMIT ?
                """, (status, limit))
            else:
                cursor.execute("""
                    SELECT e.*, u.full_name as employee_name, u.email as employee_email,
                           u.department as employee_department
                    FROM expenses e
                    JOIN users u ON e.employee_id = u.id
                    ORDER BY e.submitted_at DESC
                    LIMIT ?
                """, (limit,))
            rows = cursor.fetchall()
            return [dict_from_row(row) for row in rows]
    
    @staticmethod
    def update_expense_status(expense_id: int, status: str) -> bool:
        """
        Update the status of an expense.
        Also updates the updated_at timestamp.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE expenses 
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (status, expense_id))
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def update_expense(expense_id: int, **kwargs) -> bool:
        """
        Update expense fields dynamically.
        Returns True if successful, False otherwise.
        """
        if not kwargs:
            return False
        
        kwargs['updated_at'] = datetime.now().isoformat()
        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
        values = list(kwargs.values()) + [expense_id]
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"UPDATE expenses SET {set_clause} WHERE id = ?", values)
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def delete_expense(expense_id: int) -> bool:
        """
        Delete an expense from the database.
        Only allowed if status is 'Pending'.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id = ? AND status = 'Pending'", (expense_id,))
            conn.commit()
            return cursor.rowcount > 0


# ==================== APPROVAL MODEL ====================

class ApprovalModel:
    """
    Approval model for database operations.
    Handles CRUD operations for approvals table.
    """
    
    @staticmethod
    def create_approval(expense_id: int, approver_id: int, approval_level: int) -> int:
        """
        Create a new approval record in the database.
        Returns the created approval's ID.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO approvals (expense_id, approver_id, approval_level, status)
                VALUES (?, ?, ?, 'Pending')
            """, (expense_id, approver_id, approval_level))
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def get_approvals_by_expense(expense_id: int) -> List[Dict[str, Any]]:
        """
        Get all approval records for a specific expense.
        Returns approvals with approver details.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.*, u.full_name as approver_name, u.email as approver_email, u.role as approver_role
                FROM approvals a
                JOIN users u ON a.approver_id = u.id
                WHERE a.expense_id = ?
                ORDER BY a.approval_level, a.created_at
            """, (expense_id,))
            rows = cursor.fetchall()
            return [dict_from_row(row) for row in rows]
    
    @staticmethod
    def get_approvals_by_approver(approver_id: int, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all approval requests for a specific approver.
        Optionally filter by approval status.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute("""
                    SELECT a.*, e.amount, e.currency, e.category, e.description, e.expense_date,
                           u.full_name as employee_name, u.email as employee_email
                    FROM approvals a
                    JOIN expenses e ON a.expense_id = e.id
                    JOIN users u ON e.employee_id = u.id
                    WHERE a.approver_id = ? AND a.status = ?
                    ORDER BY a.created_at DESC
                """, (approver_id, status))
            else:
                cursor.execute("""
                    SELECT a.*, e.amount, e.currency, e.category, e.description, e.expense_date,
                           u.full_name as employee_name, u.email as employee_email
                    FROM approvals a
                    JOIN expenses e ON a.expense_id = e.id
                    JOIN users u ON e.employee_id = u.id
                    WHERE a.approver_id = ?
                    ORDER BY a.created_at DESC
                """, (approver_id,))
            rows = cursor.fetchall()
            return [dict_from_row(row) for row in rows]
    
    @staticmethod
    def update_approval_status(approval_id: int, status: str, comments: Optional[str] = None) -> bool:
        """
        Update the status of an approval record.
        Sets the approved_at timestamp if status is Approved or Rejected.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE approvals 
                SET status = ?, comments = ?, approved_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (status, comments, approval_id))
            conn.commit()
            return cursor.rowcount > 0
    
    @staticmethod
    def get_pending_approval_for_expense(expense_id: int, approver_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific pending approval for an expense and approver.
        Used to check if an approver has a pending approval task.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM approvals 
                WHERE expense_id = ? AND approver_id = ? AND status = 'Pending'
            """, (expense_id, approver_id))
            row = cursor.fetchone()
            return dict_from_row(row) if row else None


# ==================== APPROVAL RULES MODEL ====================

class ApprovalRuleModel:
    """
    Approval rules model for database operations.
    Handles CRUD operations for approval_rules table.
    """
    
    @staticmethod
    def create_rule(rule_name: str, rule_type: str, approval_level: int,
                   condition_value: Optional[float] = None, approver_role: Optional[str] = None,
                   approver_id: Optional[int] = None, department: Optional[str] = None) -> int:
        """
        Create a new approval rule.
        Returns the created rule's ID.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO approval_rules (rule_name, rule_type, condition_value, approver_role, 
                                          approver_id, approval_level, department, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            """, (rule_name, rule_type, condition_value, approver_role, approver_id, approval_level, department))
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def get_active_rules() -> List[Dict[str, Any]]:
        """
        Get all active approval rules.
        Returns a list of rule dictionaries.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM approval_rules WHERE is_active = 1 ORDER BY approval_level")
            rows = cursor.fetchall()
            return [dict_from_row(row) for row in rows]
    
    @staticmethod
    def get_rules_for_amount(amount: float) -> List[Dict[str, Any]]:
        """
        Get applicable rules based on expense amount.
        Used by the approval engine to determine workflow.
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM approval_rules 
                WHERE is_active = 1 
                AND rule_type = 'amount_threshold'
                AND (condition_value IS NULL OR ? <= condition_value)
                ORDER BY approval_level
            """, (amount,))
            rows = cursor.fetchall()
            return [dict_from_row(row) for row in rows]
    
    @staticmethod
    def deactivate_rule(rule_id: int) -> bool:
        """
        Deactivate an approval rule (soft delete).
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE approval_rules SET is_active = 0 WHERE id = ?", (rule_id,))
            conn.commit()
            return cursor.rowcount > 0