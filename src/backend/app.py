from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi_login import LoginManager
from pydantic import BaseModel
from pymongo import MongoClient
from passlib.context import CryptContext
from APIOverflow.src.backend.server.auth import auth_router
from APIOverflow.src.backend.classes.models import *
from APIOverflow.src.backend.server.service import *
from APIOverflow.src.backend.classes.datastore import data_store as ds

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
async def add_service(service: ServicePost):

    # Unpack request body
    request = service.model_dump()
    add_service_wrapper(request)
    return SUCCESS

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=5000)
    # Run using uvicorn app:app --reload


