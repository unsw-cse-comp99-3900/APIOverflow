from pydantic import BaseModel, EmailStr
from typing import Optional, List
from bson import ObjectId
from passlib.context import CryptContext
from pymongo import MongoClient

# Initialize MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client.local 

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    id: str
    username: str
    password: str
    email: EmailStr 
    role: str

    @classmethod
    def create(cls, username: str, password: str, email: str, role: str, db) -> None:
        hashed_password = pwd_context.hash(password)
        user_data = {
            "_id": ObjectId(), 
            "username": username,
            "password": hashed_password,
            "email": email,
            "role": role
        }
        db.users.insert_one(user_data)

    @classmethod
    def get(cls, username: str, db) -> Optional[dict]:
        return db.users.find_one({"username": username})

class Service(BaseModel):
    service_id: str
    name: str
    provider_username: str
    documentation: str
    endpoint: str

    @classmethod
    def get_services_by_provider(cls, username: str, db) -> List[dict]:
        return list(db.services.find({"provider_username": username}))

    @classmethod
    def get_service_by_id(cls, service_id: str, db) -> Optional[dict]:
        """Retrieve a specific service by its ID."""
        return db.services.find_one({"service_id": service_id})

    @classmethod
    def create(cls, service_data: dict, db) -> None:
        """Create a new service in the database."""
        db.services.insert_one(service_data)

    @classmethod
    def delete_service(cls, service_id: str, db) -> bool:
        result = db.services.delete_one({"service_id": service_id})
        return result.deleted_count > 0

