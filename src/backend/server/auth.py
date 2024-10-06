from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_login import LoginManager
from pydantic import BaseModel
from passlib.context import CryptContext
from src.backend.classes.models import User, db
from src.backend.classes.datastore import data_store
from typing import Union, List

auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET = 'supersecretkey'
manager = LoginManager(SECRET, token_url='/auth/login')

@manager.user_loader()
def load_user(username: str):
    user = User.get(username, db)
    return user

class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "account user"

class LoginModel(BaseModel):
    username: str
    password: str

# Login route
@auth_router.post("/login")
def login(credentials: LoginModel):
    username = credentials.username
    password = credentials.password

    user = User.get(username, db)
    if not user or not pwd_context.verify(password, user['password']):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = manager.create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer"}

# Register route
@auth_router.post("/register")
def register(user: UserCreate): 
    if User.get(user.username, db):
        raise HTTPException(status_code=400, detail="Username already taken")

    User.create(user.username, user.password, user.role, db)
    data_store.add_user(User)
    return {"message": "User created successfully"}

# Role depend routes
def role_required(roles: Union[str, List[str]]):
    if isinstance(roles, str):
        roles = [roles]

    def role_checker(user=Depends(manager)):
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        if user["role"] not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        return user

    return role_checker

# Example privileged routes
@auth_router.get("/admin")
def admin_route(user: User = Depends(manager), role: str = Depends(role_required("admin"))):
    return {"message": "Welcome, Admin!"}

@auth_router.get("/service")
def service_provider_route(user: User = Depends(manager), role: str = Depends(role_required("service provider"))):
    return {"message": "Welcome, Service Provider!"}

@auth_router.get("/account")
def account_user_route(user: User = Depends(manager), role: str = Depends(role_required("account user"))):
    return {"message": "Welcome, Account User!"}

@auth_router.get("/guest")
def guest_route(user: User = Depends(manager), role: str = Depends(role_required("guest"))):
    return {"message": "Welcome, Guest!"}
