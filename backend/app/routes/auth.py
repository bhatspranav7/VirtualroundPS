from fastapi import APIRouter
from passlib.context import CryptContext
import sqlite3
from ..config import DATABASE_PATH

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
