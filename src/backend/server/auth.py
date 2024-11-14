from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_login import LoginManager
from pydantic import BaseModel
from passlib.context import CryptContext
from src.backend.classes.datastore import data_store
from src.backend.classes.User import User
from typing import Literal, TypeVar
from src.backend.database import *
from src.backend.classes.Manager import manager, SECRET, blacklisted_tokens
import jwt
from datetime import datetime, timedelta, timezone
import os
from oauth2client import client, tools, file
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
import base64
from dotenv import load_dotenv
from pathlib import Path
import os
from src.backend.server.email import send_email

current_dir = os.path.dirname(os.path.abspath(__file__))

T = TypeVar("T")
ADMIN = 'admin'
GENERAL = 'general'

def load_email_setting():
    load_dotenv(Path(__file__).parent.parent / '.env')
    return os.getenv("EMAIL") == "True"
email = load_email_setting()

def generate_verification_token(uid: str) -> str:
    expiration_time = datetime.now(timezone.utc) + timedelta(minutes=30)
    token = jwt.encode({"sub": uid, "exp": expiration_time}, SECRET, algorithm="HS256")
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    
# Login route
def login_wrapper(username: str, password: str, verify: bool = email) -> T:
    '''
        Wrapper used to handle logging in
    '''
    if data_store.num_users() == 0:
        create_super_admin()
    user = data_store.get_user_by_name(username)
    if not user or not manager.verify_password(password, user.get_password()):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if verify:
        if not user.get_is_verified():
            raise HTTPException(status_code=403, detail="Email not verified")

    access_token = manager.create_access_token(data={"sub": user.get_id()})
    user.update_token(access_token)

    if access_token in blacklisted_tokens:
        del blacklisted_tokens[access_token]
    return access_token

def register_wrapper(displayname: str, name: str, password: str, email: str, verify: bool = email) -> str:
    '''
        Handles registering a new user    
    '''
    if data_store.num_users() == 0:
        create_super_admin()
    if data_store.get_user_by_name(name):
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = User(str(data_store.max_num_users()),
                    displayname, 
                    name,
                    manager.hash_password(password),
                    email,
                    False,
                    False)
    db_add_user(new_user.to_json())
    data_store.add_user(new_user)

    if verify:
        verification_token = generate_verification_token(new_user.get_id())
        send_email(email, verification_token)

    return new_user.get_id()

def create_super_admin() -> None:
    '''
        Creates a super admin at web-app creation   
    '''
    super_admin = User(str(data_store.max_num_users()),
                    "superadmin",
                    "superadmin",
                    manager.hash_password("superadminpassword"),
                    "superadmin@gmail.com",
                    True,
                    True)
    super_admin.verify_user()
    db_add_user(super_admin.to_json())
    data_store.add_user(super_admin)

def change_password(uid: str, newpass: str) -> None:
    '''
        Allows the user to change their own password  
    '''
    user = data_store.get_user_by_id(uid)
    user.change_password(manager.hash_password(newpass))
    db_update_user(uid, user.to_json())

def password_reset_request(uid: str, verify: bool = email) -> None:
    '''
        Handles password reset request  
    '''
    user = data_store.get_user_by_id(uid)
    if verify:
        verification_token = generate_verification_token(user.get_id())
        send_email(user.get_email(), verification_token, 'password_reset')