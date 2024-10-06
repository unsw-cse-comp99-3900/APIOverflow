from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi_login import LoginManager
from pydantic import BaseModel
from pymongo import MongoClient
from passlib.context import CryptContext
from src.backend.server.auth import auth_router
from src.backend.classes.models import *
from src.backend.server.service import *
from src.backend.classes.datastore import data_store as ds

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
    return {"message" : "Clear Successful"}

# Include authentication router
app.include_router(auth_router, prefix="/auth")



@app.post("/service/add")
async def add_service(service: ServicePost, user=Depends(manager)):
    '''
        Method used to add service to platform
    '''
    # Unpack request body
    request = service.model_dump()
    uid = user['_id']
    add_service_wrapper(request, str(uid))


@app.get("service/get_service")
async def get_service(sid: str, user=Depends(manager)):
    '''
        Method to retrieve a particular service
    '''
    uid = user['_id']
    response = get_service_wrapper(sid, str(uid))
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
    # Run using uvicorn app:app --reload


