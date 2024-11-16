from typing import Literal, TypeVar
import os
from oauth2client import client, tools, file
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
import base64
from dotenv import load_dotenv
from pathlib import Path
import os

app_host = os.getenv("APP_HOST", "localhost")
app_port = os.getenv("APP_PORT", "5000")
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
    credential_dir = os.path.join(current_dir, '.credentials')
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

def send_email(to_email: str, token: str, email_type: str = 'verification', content: dict = {}):
    """Send an email with HTML and plain text content."""
    sender_email = "api.overflow6@gmail.com"
    
    root_link = f"http://{app_host}:{app_port}/auth"
    if email_type == 'verification':
        verification_link = f"{root_link}/verify-email/{token}"
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
        reset_link = f"{root_link}/reset-password/{token}"
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

    elif email_type == 'service_approval':
        action = content['action']
        service_name = content['sname']
        user_name = content['uname']
        if action == 'approved':
            tone = 'pleased'
        else:
            tone = 'regret'
        subject = "Service Upload Outcome"
        msg_html = f"""
        Hi {user_name},<br/>
        We are {tone} to inform you that your service - {service_name} has been {action}.<br/>
        Thank you for your contribution to API Overflow.<br/>
        Best regards,<br/>
        API Overflow Team
        """
        msg_plain = f"Hi {user_name},\nWe are {tone} to inform you that your service - {service_name} has been {action}." \
        f"Thank you for your contribution to API Overflow.\nBest regards,\nAPI Overflow Team"
    
    elif email_type == 'account_deleted':
        action = content['action']
        user_name = content['uname']
        if action == 'admin':
            outcome = 'by an admin'
        else:
            outcome = 'successfully'
        subject = "API Overflow Account Deleted"
        msg_html = f"""
        Hi {user_name},<br/>
        Your account has been deleted {outcome}.<br/>
        Please contact this email if you think there has been an error.<br/>
        Best regards,<br/>
        API Overflow Team
        """
        msg_plain = f"Hi {user_name},\nYour account has been deleted {outcome}." \
        f"Please contact this email if you think there has been an error.\nBest regards,\nAPI Overflow Team"

    elif email_type == 'reivew_reply':
        action = content['action']
        msg = content['msg']
        if len(msg) > 80:
            msg = msg[:80] + "..."
        msg = '"' + msg + '"'
        subject_name = content['subname']
        related_name = content['rname']
        service_name = content['sname']
        subject = "Service Review Update"
        msg_html = f"""
        Hi {subject_name},<br/>
        You have recieved a {action} from {related_name} regarding {service_name}:<br/>
        {msg}.<br/>
        Best regards,<br/>
        API Overflow Team
        """
        msg_plain = f"Hi {subject_name},\nYou have recieved a {action} from {related_name} regarding {service_name}:" \
        f"{msg}.\nBest regards,\nAPI Overflow Team"

    else:
        raise ValueError("Invalid email type specified.")

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