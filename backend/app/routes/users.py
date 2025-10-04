# backend/app/routes/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def list_users():
    # Placeholder sample data
    return [{"id": 1, "name": "Admin", "role": "Admin"}]
