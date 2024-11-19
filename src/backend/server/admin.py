from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_login import LoginManager
from pydantic import BaseModel
from passlib.context import CryptContext
from src.backend.classes.datastore import data_store
from src.backend.classes.User import User
from typing import Literal, TypeVar, List
from src.backend.database import *
from src.backend.classes.Manager import manager
from src.backend.classes.Service import PENDING_OPTIONS
from src.backend.server.email import send_email

T = TypeVar("T")
ADMIN = 'admin'
GENERAL = 'general'

def is_valid_user(uid: str):
    if uid == '':
        raise HTTPException(status_code=400, detail='No user id provided')

    user = data_store.get_user_by_id(uid)
    if user is None:
        raise HTTPException(status_code=404, detail='No user found with given uid')


def promote_user(uid: str, is_super: bool):
    is_valid_user(uid)
    user = data_store.get_user_by_id(uid)
    if user.get_is_admin():
        raise HTTPException(status_code=400, detail=f"User {user.get_name()} is already an admin.")
    if is_super:
        user.promote_to_admin()
    else:
        raise HTTPException(status_code=403, detail="Only Superadmin can promote users.")
    db_update_user(uid, user.to_json())
    username = user.get_name()
    return {"name": username, "status": user.get_is_admin()}

def demote_user(uid: str, is_super: bool):
    is_valid_user(uid)
    user = data_store.get_user_by_id(uid)
    if not user.get_is_admin():
        raise HTTPException(status_code=400, detail=f"User {user.get_name()} is not an admin.")
    target_is_super = user.get_is_super()
    if is_super and not target_is_super:
        user.demote_to_user()
    else:
        raise HTTPException(status_code=403, detail="Admins cannot demote other Admins.")
    username = user.get_name()
    db_update_user(uid, user.to_json())
    return {"name": username, "status": not user.get_is_admin()}

def delete_user(uid: str, is_super: bool):
    is_valid_user(uid)
    user = data_store.get_user_by_id(uid)
    username = user.get_name()
    target_is_super = user.get_is_super()
    target_is_admin = user.get_is_admin()
    if (is_super and not target_is_super):
        data_store.delete_item(uid, 'user')
        db_status = db_delete_user(username)
    else:
        if target_is_super:
            raise HTTPException(status_code=403, detail="Admins cannot delete the Super Admin.")
        elif target_is_admin:
            raise HTTPException(status_code=403, detail="Admins cannot delete other Admins.")
        else:
            data_store.delete_item(uid, 'user')
            db_status = db_delete_user(username)
    action = "admin"
    uname = username
    uemail = user.get_email()
    content = {'action': action, 'uname': uname}
    send_email(uemail, '', 'account_deleted', content)
    return {"name": username, "deleted": db_status}

def get_all_users():
    users = data_store.get_users()
    users_json = [user.to_json(include_password=False) for user in users]
    return {"users": users_json, "user_count": data_store.num_users()}

def admin_filter_users(standard: bool, admin: bool, super: bool):
    users = data_store.get_users()
    return_list = []
    if standard:
        for user in users:
            if not user.get_is_admin():
                return_list.append(user.to_json())
    if admin:
        for user in users:
            if user.get_is_admin() and user.to_json() not in return_list:
                return_list.append(user.to_json())
    if super:
        for user in users:
            if user.get_is_super() and user.to_json() not in return_list:
                return_list.append(user.to_json())
    return return_list
        
def admin_get_reviews_wrapper() -> List[dict[str, str]]:
    '''
        Wrapper which returns all reviews which are pending 
    '''
    reviews = []
    for review in data_store.get_reviews():
        reviews.append(review.to_json(brief=True))
    
    return reviews

def admin_get_pending_services() -> List[dict[str, str]]:
    '''
        Wrapper which returns all reviews which are pending 
    '''
    new_services = []
    global_updates = []
    version_updates = []

    for service in data_store.get_apis():    

        if service.get_status() in PENDING_OPTIONS:
            if service.get_newly_created():
                new_service_json = service.to_updated_json()
                new_service_json["version_fields"] = service.get_latest_version(
                ).to_updated_json(service.get_id(), service.get_name())
                new_services.append(new_service_json)
                continue
            else:
                global_updates.append(service.to_updated_json())
        
        for version in service.get_all_versions():
            if version.get_status() in PENDING_OPTIONS:
                version_updates.append(version.to_updated_json(service.get_id(), service.get_name()))

    return {
        "new_services": new_services,
        "global_updates": global_updates,
        "version_updates": version_updates
    }

def admin_check_if_admin(uid: str):
    is_valid_user(uid)
    user = data_store.get_user_by_id(uid)
    username = user.get_name()
    target_is_super = user.get_is_super()
    target_is_admin = user.get_is_admin()
    return {"name": username, "is_admin": target_is_admin, "is_super": target_is_super}
    
