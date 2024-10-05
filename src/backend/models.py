from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
from pymongo import MongoClient

# Initialize MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client.local 

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    password: str
    role: str

    @classmethod
    def create(cls, username: str, password: str, role: str, db) -> None:
        hashed_password = pwd_context.hash(password)
        user_data = {"username": username, "password": hashed_password, "role": role}
        db.users.insert_one(user_data)

    @classmethod
    def get(cls, username: str, db) -> Optional[dict]:
        return db.users.find_one({"username": username})

