from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi_login import LoginManager
from pydantic import BaseModel
from pymongo import MongoClient
from passlib.context import CryptContext
from auth import auth_router, service_router
from models import User

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

# Include authentication router
app.include_router(auth_router, prefix="/auth")
app.include_router(service_router, prefix="/service")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
    # Run using uvicorn app:app --reload
