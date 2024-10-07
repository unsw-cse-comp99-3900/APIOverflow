from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi_login import LoginManager
from pydantic import BaseModel
from pymongo import MongoClient
from passlib.context import CryptContext
from src.backend.classes.models import *
from src.backend.server.service import *
from src.backend.classes.datastore import data_store as ds
from src.backend.server.auth import *
from src.backend.classes.Manager import manager

app = FastAPI()

SECRET = 'supersecretkey'

client = MongoClient('mongodb://localhost:27017')
db = client.local

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

manager = LoginManager(SECRET, token_url='/auth/login')
@manager.user_loader()
def load_user(username: str):
    user = User.get(username, db)
    return user

@app.get("/")
async def home():
    return {
        "message": "Welcome to the MongoDB Auth System.",
        "login_link": "/auth/login",
        "register_link": "/auth/register"
    }

@app.post("/testing/clear")
async def clear():
    '''
        Internal Testing function to clear datastore
    '''
    ds.clear_datastore()
    assert ds.num_apis() == 0
    return {"message" : "Clear Successful"}

@app.post("/service/add")
async def add_service(service: ServicePost, user: User = Depends(manager)):
    '''
        Method used to add service to platform
    '''
    # Unpack request body
    request = service.model_dump()
    uid = user['_id']
    sid = add_service_wrapper(request, str(uid))
    return {'sid' : sid}


@app.get("/service/get_service")
async def get_service(sid: str, user: User=Depends(manager)):
    '''
        Method to retrieve a particular service
    '''
    response = get_service_wrapper(sid)
    return response

# Role depend routes
def role_required(roles: Union[str, List[str]]):
    '''
        Used to verify dependency of user roles
    '''
    if isinstance(roles, str):
        roles = [roles]

    def role_checker(user=Depends(manager)):
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        if user["role"] not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
        return user

    return role_checker

@app.post("/login")
async def login(credentials: LoginModel):
    '''
        Login a user (or attempt to)
    '''
    username = credentials.username
    password = credentials.password
    access_token = login_wrapper(username, password)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/auth/register")
async def register(user: UserCreate):
    '''
        Register a user onto the platform
    '''
    uid = register_wrapper(user.username, user.password, user.email, user.role)
    return {'uid' : uid}

# Example privileged routes
@app.get("/admin")
async def admin_route(user: User = Depends(manager), role: str = Depends(role_required("admin"))):
    return {"message": "Welcome, Admin!"}

@app.get("/service")
async def service_provider_route(user: User = Depends(manager), role: str = Depends(role_required("service provider"))):
    return {"message": "Welcome, Service Provider!"}

@app.get("/account")
async def account_user_route(user: User = Depends(manager), role: str = Depends(role_required("account user"))):
    return {"message": "Welcome, Account User!"}

@app.get("/guest")
async def guest_route(user: User = Depends(manager), role: str = Depends(role_required("guest"))):
    return {"message": "Welcome, Guest!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
    # Run using uvicorn app:app --reload

