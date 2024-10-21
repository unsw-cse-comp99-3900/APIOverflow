from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_login import LoginManager
from pydantic import BaseModel
from passlib.context import CryptContext
from src.backend.classes.datastore import data_store
from src.backend.classes.User import User
from typing import Literal, TypeVar
from src.backend.database import *
from src.backend.classes.Manager import manager


T = TypeVar("T")
ADMIN = 'admin'
GENERAL = 'general'

# Login route
def login_wrapper(username: str, password: str) -> T:
    '''
        Wrapper used to handle logging in
    '''
    user = data_store.get_user_by_name(username)
    if not user or not manager.verify_password(password, user.get_password()):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return manager.create_access_token(data={"sub": user.get_id()})

def register_wrapper(name: str, password: str, email: str, is_admin: bool) -> str:
    '''
        Handles registering a new user    
    '''
    if data_store.get_user_by_name(name):
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = User(str(data_store.num_users()),
                    name,
                    manager.hash_password(password),
                    email,
                    is_admin,
                    False)
    db_add_user(new_user.to_json())
    data_store.add_user(new_user)
    return new_user.get_id()

def create_super_admin() -> None:
    super_admin = User(str(data_store.num_users()),
                    "superadmin",
                    manager.hash_password("superadminpassword"),
                    "superadmin@gmail.com",
                    True,
                    True)
    db_add_user(super_admin.to_json())
    data_store.add_user(super_admin)
