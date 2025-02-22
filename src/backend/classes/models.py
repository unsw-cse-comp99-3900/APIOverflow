from pydantic import BaseModel, ConfigDict
from typing import Optional
from passlib.context import CryptContext
from pymongo import MongoClient
from typing import *
from bson import ObjectId
from src.backend.database import db
from src.backend.classes.Endpoint import Endpoint

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    password: str
    is_admin: bool
    is_super: bool

    @classmethod
    def create(cls, username: str, password: str, is_admin: bool, is_super: bool, db) -> None:
        hashed_password = pwd_context.hash(password)
        user_data = {
            "_id": ObjectId(),
            "username": username,
            "password": hashed_password, 
            "is_admin": is_admin,
            "is_super": is_super}
        db.users.insert_one(user_data)

    @classmethod
    def get(cls, username: str, db) -> Optional[dict]:
        return db.users.find_one({"username": username})

class UserCreate(BaseModel):
    displayname: str
    username: str
    password: str
    email: str
    is_admin: bool = False
    is_super: bool = False

class LoginModel(BaseModel):
    username: str
    password: str

class FilterRequest(BaseModel):
    tags: List[str]
    providers: List[str]

# Request body for POST methods relating to services
class ServiceAdd(BaseModel):

    name: str                           # Name of service
    description: str                    # Descrtipion of service
    tags: List[str]                     # List of tags assigned to the service
    endpoints: List[Endpoint]           # Endpoint of the service uploaded
    version_name: str = "version 1"     # name of service version
    version_description: str = "No version description provided" # description
    pay_model: str = 'Free'             # Pay model of the service

    class Config:
        arbitrary_types_allowed = True

class ServiceAddVersion(BaseModel):

    sid: str                        # id of service 
    version_name: str               # name of new version
    endpoints: List[Endpoint]       # endpoints of new version
    version_description: str        # Additional details pertaining new version   

class ServiceUpdateVersion(BaseModel):

    sid: str                        # id of service 
    version_name: str               # name of new version
    new_version_name: Optional[str] = None # if we are renaming version 
    endpoints: List[Endpoint]       # endpoints of new version
    version_description: str        # Additional details pertaining new version   

class ServiceGlobalUpdate(BaseModel):
    name: str                       # Name of service
    description: str                # Descrtipion of service
    tags: List[str]                 # List of tags assigned to the service
    sid: str
    pay_model: str = 'Free'         # Pay model of service
    class Config:
        arbitrary_types_allowed = True

class ServiceUpload(BaseModel):

    sid: str
    version_name: Optional[str] = None
    doc_id: str
    

class TagData(BaseModel):
    tag: str

class DocumentID(BaseModel):
    doc_id: str

class ServiceIconInfo(BaseModel):
    sid: str
    doc_id: str

class ServiceIconDeleteInfo(BaseModel):
    sid: str

class Password(BaseModel):
    newpass: str

class ServiceReviewInfo(BaseModel):
    sid: str
    rating: str
    comment: str

class ServiceReviewEditInfo(BaseModel):
    rid: str
    rating: str
    comment: str

class ServiceReviewAdminAction(BaseModel):
    rid: str
    reason: str

class ServiceApprove(BaseModel):
    sid: str
    approved: bool
    reason: str
    service_global: bool          # whether we are updating global fields
    version_name: Optional[str] = None # approved version if applicable

class AdminGetReviews(BaseModel):
    option: str = ''
class ReviewPackage(BaseModel):
    rid: str
    content: str = ''
class GeneralString(BaseModel):
    content: str

class GeneralInt(BaseModel):
    num: int