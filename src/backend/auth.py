from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_login import LoginManager
from pydantic import BaseModel, HttpUrl, EmailStr
from passlib.context import CryptContext
from models import User, db, Service
from typing import Union, List, Optional
from datetime import timedelta
from bson import ObjectId

auth_router = APIRouter()
service_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET = 'supersecretkey'
manager = LoginManager(SECRET, token_url='/auth/login')

@manager.user_loader()
def load_user(user_id: str):
    user = db.users.find_one({"_id": ObjectId(user_id)})
    return user

class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    role: str = "account user"

class LoginModel(BaseModel):
    username: str
    password: str

class ServiceCreate(BaseModel):
    name: str
    documentation: str
    endpoint: str 

# Login route
@auth_router.post("/login")
def login(credentials: LoginModel):
    username = credentials.username
    password = credentials.password

    user = User.get(username, db)
    if not user or not pwd_context.verify(password, user['password']):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = manager.create_access_token(
        data={"sub": str(user["_id"])},
        expires=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

# Register route
@auth_router.post("/register")
def register(user: UserCreate): 
    if User.get(user.username, db):
        raise HTTPException(status_code=400, detail="Username already taken")

    User.create(user.username, user.password, user.email, user.role, db)
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

# Service Management Routes
@service_router.get("/manage")
def manage_services(user: User = Depends(manager), role: str = Depends(role_required("service provider"))):
    services = Service.get_services_by_provider(user["username"], db)
    return {
        "message": f"Welcome {user['username']}, you can manage your services here.",
        "services": services
    }

@service_router.post("/create")
def create_service(service_data: ServiceCreate, user: User = Depends(manager), role: str = Depends(role_required("service provider"))):
    service_dict = service_data.model_dump()
    service_dict['provider_username'] = user['username']
    
    service_dict['service_id'] = str(ObjectId())
    Service.create(service_dict, db)
    return {
        "message": f"Service '{service_data.name}' created by {user['username']}.",
        "service_id": service_dict['service_id']
    }


@service_router.delete("/delete/{service_id}")
def delete_service(service_id: str, user: User = Depends(manager), role: str = Depends(role_required(["service provider", "admin"]))):
    service = Service.get_service_by_id(service_id, db)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    if service['provider_username'] != user['username']:
        raise HTTPException(status_code=403, detail="Not authorized to delete this service")

    if Service.delete_service(service_id, db):
        return {"message": "Service deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete service")

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
