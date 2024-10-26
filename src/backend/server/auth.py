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
import os
from oauth2client import client, tools, file
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
import base64
from dotenv import load_dotenv
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))

T = TypeVar("T")
ADMIN = 'admin'
GENERAL = 'general'

def load_email_setting():
    load_dotenv(Path(__file__).parent.parent / '.env')
    return os.getenv("EMAIL") == "True"
email = load_email_setting()

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
APPLICATION_NAME = 'Gmail API Python Send Email'
CLIENT_SECRET_FILE = os.path.join(current_dir, "secret.json")

def get_credentials():
    credential_dir = os.path.join(os.path.expanduser('~'), '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'api-overflow-gmail.json')
    store = file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        flags = tools.argparser.parse_args([])
        credentials = tools.run_flow(flow, store, flags)
    return credentials

def send_email(to_email: str, token: str, email_type: str = 'verification'):
    """Send an email with HTML and plain text content."""
    sender_email = "api.overflow6@gmail.com"

    if email_type == 'verification':
        verification_link = f"http://localhost:8000/auth/verify-email/{token}"
        subject = "Please Verify Your Email Address"
        msg_html = f"""
        Hi,<br/>
        Thank you for registering! Please click the link below to verify your email address:<br/>
        <a href="{verification_link}">Verify Email</a><br/>
        If you did not create an account, please ignore this email.<br/>
        Best regards,<br/>
        API Overflow Team
        """
        msg_plain = "Hi,\nThank you for registering! Please click the link below to verify your email address:\n" \
                    f"{verification_link}\nIf you did not create an account, please ignore this email.\nBest regards,\nAPI Overflow Team"

    elif email_type == 'password_reset':
        reset_link = f"http://localhost:8000/auth/reset-password/{token}"
        subject = "Password Reset Request"
        msg_html = f"""
        Hi,<br/>
        We received a request to reset your password. Please click the link below to reset it:<br/>
        <a href="{reset_link}">Reset Password</a><br/>
        If you did not request a password reset, please ignore this email.<br/>
        Best regards,<br/>
        API Overflow Team
        """
        msg_plain = "Hi,\nWe received a request to reset your password. Please click the link below to reset it:\n" \
                    f"{reset_link}\nIf you did not request a password reset, please ignore this email.\nBest regards,\nAPI Overflow Team"

    else:
        raise ValueError("Invalid email type specified. Use 'verification' or 'password_reset'.")

    try:
        credentials = get_credentials()
        service = build('gmail', 'v1', credentials=credentials)

        message = create_message_html(sender_email, to_email, subject, msg_html, msg_plain)

        result = send_message_internal(service, "me", message)
        return result

    except Exception as e:
        print(f"Failed to send email: {e}")
        return None

def create_message_html(sender, to, subject, msg_html, msg_plain):
    """Create a MIME message in HTML and plain text format."""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg.attach(MIMEText(msg_plain, 'plain'))
    msg.attach(MIMEText(msg_html, 'html'))
    return {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}

def send_message_internal(service, user_id, message):
    """Send an email message."""
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print('An error occurred: %s' % error)
        return "Error"

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
    user = data_store.get_user_by_name(username)
    if not user or not manager.verify_password(password, user.get_password()):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    if verify:
        if not user.get_is_verified():
            raise HTTPException(status_code=403, detail="Email not verified")

    return manager.create_access_token(data={"sub": user.get_id()})

def register_wrapper(name: str, password: str, email: str, is_admin: bool, verify: bool = email) -> str:
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
    super_admin.verify_user()
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

def password_reset_request(uid: str, verify: bool = email) -> None:
    '''
        Handles password reset request  
    '''
    user = data_store.get_user_by_id(uid)
    if verify:
        verification_token = generate_verification_token(user.get_id())
        send_email(user.get_email(), verification_token, 'password_reset')