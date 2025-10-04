from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
from passlib.context import CryptContext
from ..config import DATABASE_PATH

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Request body schemas
class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    email: str
    full_name: str
    password: str
    role: str  # 'Admin', 'Manager', or 'Employee'
    manager_id: int | None = None
    department: str | None = None

# Helper to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Helper to hash password
def hash_password(password):
    return pwd_context.hash(password)

# ---------------- Register endpoint ----------------
@router.post("/register")
def register(user: UserRegister):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = hash_password(user.password)
    cursor.execute(
        """INSERT INTO users (email, hashed_password, full_name, role, manager_id, department)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (user.email, hashed_pwd, user.full_name, user.role, user.manager_id, user.department)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, "email": user.email, "full_name": user.full_name, "role": user.role}

# ---------------- Login endpoint ----------------
@router.post("/login")
def login(credentials: UserLogin):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, email, hashed_password FROM users WHERE email = ?", (credentials.email,))
    user = cursor.fetchone()
    conn.close()

    if not user or not verify_password(credentials.password, user[2]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # For simplicity, returning a dummy token. You can replace with JWT.
    return {"message": f"User {user[1]} logged in successfully", "token": "dummy-token"}
