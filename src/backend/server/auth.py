from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_login import LoginManager
from pydantic import BaseModel
from passlib.context import CryptContext
from src.backend.classes.datastore import data_store
from src.backend.classes.User import User
from typing import Literal, TypeVar
from src.backend.database import *
from src.backend.classes.Manager import manager, SECRET
import jwt
from datetime import datetime, timedelta, timezone
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

T = TypeVar("T")
ADMIN = 'admin'
GENERAL = 'general'

def send_email(email: str, token: str, email_type: str = 'verification'):
    sender_email = "api.overflow6@gmail.com"
    sender_password = "itdobeflowing"

    if email_type == 'verification':
        verification_link = f"http://localhost:8000/auth/verify-email/{token}"
        subject = "Please Verify Your Email Address"
        body = f"""
        Hi,

        Thank you for registering! Please click the link below to verify your email address:

        {verification_link}

        If you did not create an account, please ignore this email.

        Best regards,
        API Overflow Team
        """
    elif email_type == 'password_reset':
        reset_link = f"http://localhost:8000/auth/reset-password/{token}"
        subject = "Password Reset Request"
        body = f"""
        Hi,

        We received a request to reset your password. Please click the link below to reset it:

        {reset_link}

        If you did not request a password reset, please ignore this email.

        Best regards,
        API Overflow Team
        """
    else:
        raise ValueError("Invalid email type specified. Use 'verification' or 'password_reset'.")

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
        print("Message created.")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            print(f"Connecting to SMTP server... {server.ehlo()}")
            server.login(sender_email, sender_password)
            print("Logged in successfully.")
            server.sendmail(sender_email, email, msg.as_string())
            print("Email sent.")
            server.close()

        print("Verification email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

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
def login_wrapper(username: str, password: str, verify: bool = False) -> T:
    '''
        Wrapper used to handle logging in
    '''
    user = data_store.get_user_by_name(username)
    if not user or not manager.verify_password(password, user.get_password()):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if verify:
        if not user.get_is_verified():
            raise HTTPException(status_code=403, detail="Email not verified")

    return manager.create_access_token(data={"sub": user.get_id()})

def register_wrapper(name: str, password: str, email: str, is_admin: bool, verify: bool = False) -> str:
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

    if verify:
        verification_token = generate_verification_token(new_user.get_id())
        send_email(email, verification_token)

    return new_user.get_id()

def create_super_admin() -> None:
    '''
        Creates a super admin at web-app creation   
    '''
    super_admin = User(str(data_store.num_users()),
                    "superadmin",
                    manager.hash_password("superadminpassword"),
                    "superadmin@gmail.com",
                    True,
                    True)
    db_add_user(super_admin.to_json())
    data_store.add_user(super_admin)

def self_delete(uid: str) -> None:
    '''
        Allows the user to delete their own account  
    '''
    user = data_store.get_user_by_id(uid)
    username = user.get_name()
    data_store.delete_item(uid, 'user')
    db_delete_user(username)

def change_password(uid: str, newpass: str) -> None:
    '''
        Allows the user to change their own password  
    '''
    user = data_store.get_user_by_id(uid)
    user.change_password(manager.hash_password(newpass))
    db_update_user(uid, user.to_json())

def password_reset_request(uid: str, verify: bool = False) -> None:
    '''
        Handles password reset request  
    '''
    user = data_store.get_user_by_id(uid)
    if verify:
        verification_token = generate_verification_token(user.get_id())
        send_email(user.get_email(), verification_token, 'password_reset')