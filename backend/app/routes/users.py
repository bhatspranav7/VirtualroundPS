from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
import sqlite3
from ..config import DATABASE_PATH

router = APIRouter(prefix="/api/users", tags=["Users"])

class User(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    manager_id: int | None = None
    department: str | None = None

@router.get("/", response_model=List[User])
async def get_users():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, full_name, role, manager_id, department FROM users")
        users = cursor.fetchall()
    return [User(id=u[0], email=u[1], full_name=u[2], role=u[3], manager_id=u[4], department=u[5]) for u in users]

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, full_name, role, manager_id, department FROM users WHERE id=?", (user_id,))
        user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(id=user[0], email=user[1], full_name=user[2], role=user[3], manager_id=user[4], department=user[5])
