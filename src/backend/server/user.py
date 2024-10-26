from typing import TypeVar
from fastapi import File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from PIL import Image
import urllib.request
from urllib.error import HTTPError, URLError
from src.backend.classes.datastore import data_store
from src.backend.classes.API import API
from src.backend.database import *
import re

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

    icon_id = user.get_icon()
    return {
        'icon' : user.get_icon(),
    }

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
