from typing import TypeVar, List
from fastapi import File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from PIL import Image
import urllib.request
from urllib.error import HTTPError, URLError
from src.backend.classes.datastore import data_store
from src.backend.classes.API import API
from src.backend.database import *
import re
from src.backend.server.email import send_email
from src.backend.server.service import delete_service
from src.backend.server.review import review_delete_wrapper, review_remove_vote_wrapper
from src.backend.classes.Manager import blacklist_user_token

def user_add_icon_wrapper(uid: str, doc_id: str) -> None:
    '''
        Wrapper which handles a user adding an icon to their profile
    '''

    # Grab user
    user = data_store.get_user_by_id(uid)
    if user is None:
        raise HTTPException(status_code=404, detail="No such user found")

    # Grab image
    icon = data_store.get_doc_by_id(doc_id)
    if icon is None:
        raise HTTPException(status_code=404, detail="No such icon found")
    
    # Link icon with user
    user.modify_icon(doc_id)

def user_delete_icon_wrapper(uid: str) -> None:
    '''
        Wrapper which handles a user deleting their icon
    '''
    # Grab user
    user = data_store.get_user_by_id(uid)
    if user is None:
        raise HTTPException(status_code=404, detail="No such user found")

    # Remove icon (restore to default)
    user.remove_icon()

def user_get_wrapper(uid: str):
    '''
        Grabs user information - currently a dummy endpoint wrapper    
    '''
    # Grab user
    user = data_store.get_user_by_id(uid)
    if user is None:
        raise HTTPException(status_code=404, detail="No such user found")

    return user.to_summary_json()

def user_get_icon_wrapper(uid: str) -> FileResponse:
    '''
        Wrapper which returns user's icon file
    '''
    # Grab user
    user = data_store.get_user_by_id(uid)
    if user is None:
        raise HTTPException(status_code=404, detail="No such user found")

    icon_id = user.get_icon()
    icon = data_store.get_doc_by_id(icon_id)
    return FileResponse(icon.get_path())

def user_get_reviews_wrapper(uid: str) -> List[dict[str, str]]:
    '''
        Wrapper which returns user's reviews
    '''
    # Grab user
    user = data_store.get_user_by_id(uid)
    if user is None:
        raise HTTPException(status_code=404, detail="No such user found")

    reviews = []
    for rid in user.get_reviews():
        review = data_store.get_review_by_id(rid)
        json = review.to_json(brief=True)
        json['reviewerName'] = user.get_displayname()
        reviews.append(json)
    return reviews

def user_get_profile_wrapper(uid: str) -> dict[str, str]:
    '''
        Wrapper which returns profile information of user
    '''

    # Grab user
    user = data_store.get_user_by_id(uid)
    if user is None:
        raise HTTPException(status_code=404, detail="No such user found")

    return user.get_profile()

def user_self_delete(uid: str):
    '''
        Allows the user to delete their own account  
    '''
    user = data_store.get_user_by_id(uid)
    if user is None:
        raise HTTPException(status_code=404, detail="No such user found")
    username = user.get_name()
    user_delete_association(uid)
    data_store.delete_item(uid, 'user')
    db_status = db_delete_user(username)
    action = "self"
    uname = username
    uemail = user.get_email()
    content = {'action': action, 'uname': uname}
    send_email(uemail, '', 'account_deleted', content)

    return {"name": username, "deleted": db_status}

def user_delete_association(uid: str):
    user = data_store.get_user_by_id(uid)
    upvoted_review_ids = user.get_upvotes()
    downvoted_review_ids = user.get_downvotes()
    print(upvoted_review_ids)
    print(downvoted_review_ids)
    for rid in upvoted_review_ids:
        review_remove_vote_wrapper(rid, uid)

    for rid in downvoted_review_ids:
        review_remove_vote_wrapper(rid, uid)
    
    review_ids = user.get_reviews()
    for rid in review_ids:
        review_delete_wrapper(rid, '0', True) 

    service_ids = user.get_services()
    for sid in service_ids:
        delete_service(sid)

    blacklist_user_token(uid)

def user_update_displayname(uid: str, new: str) -> None:
    '''
        Allows the user to update their displayname
    '''
    user = data_store.get_user_by_id(uid)
    if user is None:
        raise HTTPException(status_code=404, detail="No such user found")
    user.modify_displayname(new)
    db_update_user(uid, user.to_json())

    return {"displayname": new, "updated": True}

def user_get_replies_wrapper(uid: str) -> List[dict[str, str]]:
    '''
        Wrapper which returns a list of all replies made by the user
    ''' 
    
    # Check if user exists
    user = data_store.get_user_by_id(uid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    replies = user.get_replies()
    output = []
    for _reply in replies:
        reply = data_store.get_reply_by_id(_reply).to_json()
        reply['reviewerName'] = user.get_displayname()
        output.append(reply)
    return {
        'replies' : output

    }
