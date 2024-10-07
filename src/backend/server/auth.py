from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_login import LoginManager
from pydantic import BaseModel
from passlib.context import CryptContext
from src.backend.classes.datastore import data_store
from src.backend.classes.User import User
from typing import Union, List, TypeVar
from src.backend.database import *
from src.backend.classes.Manager import manager

T = TypeVar("T")

# auth_router = APIRouter()
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# SECRET = 'supersecretkey'
# manager = LoginManager(SECRET, token_url='/auth/login')

# @manager.user_loader()
# def load_user(username: str):
#     user = User.get(username, db)
#     return user

# Login route
def login_wrapper(username: str, password: str) -> T:
    '''
        Wrapper used to handle logging in
    '''
    user = data_store.get_user_by_name(username)
    print("Auth: username=%s | user found: %s", username, user)
    if not user or not manager.verify_password(password, user.get_password()):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    return manager.create_access_token(data={"sub": user.get_id()})

# @auth_router.post("/login")
# def login(credentials: LoginModel):
#     username = credentials.username
#     password = credentials.password

#     user = User.get(username, db)
#     if not user or not pwd_context.verify(password, user['password']):
#         raise HTTPException(status_code=400, detail="Invalid username or password")

#     access_token = manager.create_access_token(data={"sub": username})
#     return {"access_token": access_token, "token_type": "bearer"}

def register_wrapper(name: str, password: str, email: str, role: str) -> str:
    '''
        Handles registering a new user    
    '''
    if data_store.get_user_by_name(name):
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = User(data_store.num_users(),
                    name,
                    manager.hash_password(password),
                    email,
                    role)
    db_add_user(new_user.to_json())
    data_store.add_user(new_user)
    return new_user.get_id()

# # Register route
# @auth_router.post("/register")
# def register(user: UserCreate): 
#     if User.get(user.username, db):
#         raise HTTPException(status_code=400, detail="Username already taken")

#     User.create(user.username, user.password, user.role, db)
#     data_store.add_user(User)
#     return {"message": "User created successfully"}




