from typing import TypeVar
from fastapi import File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from PIL import Image
import urllib.request
from urllib.error import HTTPError, URLError
from src.backend.classes.datastore import data_store
from src.backend.classes.API import API
from src.backend.database import *
from src.backend.classes.models import ServiceReviewEditInfo
from src.backend.classes.Review import *
import re

def review_get_wrapper(rid: str) -> dict[str, str]:
    '''
        Wrapper which retrieves a review
    '''
    
    # Grab review
    review = data_store.get_review_by_id(rid)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return review.to_json()

def review_delete_wrapper(rid: str, uid: str, is_admin: bool) -> None:
    '''
        Wrapper which deletes a review
    '''
    # Grab review
    review = data_store.get_review_by_id(rid)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    # Check permissions
    if review.get_reviewer() != uid and not is_admin: 
        raise HTTPException(status_code=403, detail="No permission to delete review")

    # Delete review
    user = data_store.get_user_by_id(review.get_reviewer())
    service = data_store.get_api_by_id(review.get_service())
    user.remove_review(rid)
    service.remove_review(rid, review.get_rating())
    data_store.delete_item(rid, 'review')

def review_edit_wrapper(info: ServiceReviewEditInfo, uid: str, is_admin: bool) -> None:
    '''
        Wrapper which edits a given review
    '''
    rid = info.rid
    rating = info.rating
    title = info.title
    comment = info.comment

    # Grab review
    review = data_store.get_review_by_id(rid)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

     # Check permissions
    if review.get_reviewer() != uid and not is_admin:
        raise HTTPException(status_code=403, detail="No permission to edit review")

    # Check validity of input
    if rating == '' or title == '' or comment == '':
         raise HTTPException(status_code=400, detail="Rating/Title/Comment is empty")

    if rating not in ['positive', 'negative']:
         raise HTTPException(status_code=400, detail="Invalid rating given")

    # Edit review
    review.update_review(title, rating, comment)

def review_approve_wrapper(rid: str, reason: str) -> None:
    '''
        Wrapper which handles approving reviews
    '''

    # Grab review
    review = data_store.get_review_by_id(rid)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review.update_status(LIVE, reason)

def review_reject_wrapper(rid: str, reason: str) -> None:
    '''
        Wrapper which handles rejecting reviews
    '''

    # Grab review
    review = data_store.get_review_by_id(rid)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    review.update_status(REJECTED, reason)
