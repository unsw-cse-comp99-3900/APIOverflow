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
from src.backend.classes.ReviewReply import *

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
    if review.get_owner() != uid and not is_admin: 
        raise HTTPException(status_code=403, detail="No permission to delete review")

    # Delete review
    user = data_store.get_user_by_id(review.get_owner())
    service = data_store.get_api_by_id(review.get_service())
    user.remove_review(rid)
    service.remove_review(rid, review.get_rating())

    # Delete associated reply
    reply = data_store.get_reply_by_id(review.get_reply())
    if reply is not None:
        user = data_store.get_user_by_id(reply.get_owner())
        user.remove_reply(reply.get_id())
        review.remove_reply()
        data_store.delete_item(reply.get_id(), 'reply')

    data_store.delete_item(rid, 'review')

def review_edit_wrapper(info: ServiceReviewEditInfo, uid: str, is_admin: bool) -> None:
    '''
        Wrapper which edits a given review
    '''
    rid = info.rid
    rating = info.rating
    comment = info.comment

    # Grab review
    review = data_store.get_review_by_id(rid)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

     # Check permissions
    if review.get_owner() != uid and not is_admin:
        raise HTTPException(status_code=403, detail="No permission to edit review")

    # Check validity of input
    if rating == '' or comment == '':
         raise HTTPException(status_code=400, detail="Rating/Title/Comment is empty")

    if rating not in ['positive', 'negative']:
         raise HTTPException(status_code=400, detail="Invalid rating given")

    # Edit review
    review.update_review(rating, comment)

def review_vote_wrapper(rid: str, uid: str, vote: str) -> None:
    '''
        Wrapper which processes adding a vote to a review
    '''
    review = data_store.get_review_by_id(rid)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    if review.get_owner() == uid:
        raise HTTPException(status_code=403, detail="User cannot vote on their own review")

    if review.update_vote(uid, vote) is None:
        raise HTTPException(status_code=403, detail='User has already voted')


def review_remove_vote_wrapper(rid: str, uid: str) -> None:
    '''
        Wrapper which handles removing a vote to a review
    '''
    review = data_store.get_review_by_id(rid)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    if not review.remove_vote(uid):
        raise HTTPException(status_code=400, detail="User has not voted on review")

def review_add_reply_wrapper(rid: str, uid: str, comment: str) -> None:
    '''
        Wrapper which handles adding a reply to a review
    '''
    
    # Find review
    review = data_store.get_review_by_id(rid)
    if review is None:
        raise HTTPException(status_code=404, detail="Review not found")

    # Check for permission
    server = data_store.get_api_by_id(review.get_service())
    if server.get_owner() != uid:
        raise HTTPException(status_code=403, detail='User not owner of service')

    # Check if reply already made
    if review.get_reply() is not None:
        raise HTTPException(status_code=403, detail='User already replied')

    # Check content
    if comment == '':
        raise HTTPException(status_code=400, detail='Content cannot be empty')

    # Create and add reply
    reply = ReviewReply(str(data_store.total_replies()),
                        uid,
                        server.get_id(),
                        comment,
                        rid)
    user = data_store.get_user_by_id(uid)
    user.add_reply(reply.get_id())
    data_store.add_reply(reply)
    review.add_reply(reply.get_id())

def review_delete_reply_wrapper(rid: str, uid: str) -> None:
    '''
        Wrapper which handles deleting a reply to a review
    '''
    # Grab reply
    reply = data_store.get_reply_by_id(rid)
    if reply is None:
        raise HTTPException(status_code=404, detail='Reply not found')

    # Check permission
    if reply.get_owner() != uid:
        raise HTTPException(status_code=403, detail="User not owner of reply")
    
    # Delete reply
    review = data_store.get_review_by_id(reply.get_review())
    user = data_store.get_user_by_id(reply.get_owner())
    user.remove_reply(rid)
    review.remove_reply()
    data_store.delete_item(rid, 'reply')

def review_edit_reply_wrapper(rid: str, uid: str, comment: str) -> None:
    '''
        Wrapper which handles editing a reply to a review
    '''
    # Grab reply
    reply = data_store.get_reply_by_id(rid)
    if reply is None:
        raise HTTPException(status_code=404, detail='Reply not found')

    # Check permission
    if reply.get_owner() != uid:
        raise HTTPException(status_code=403, detail="User not owner of reply")
    
    # Check content
    if comment == '':
        raise HTTPException(status_code=400, detail='Content cannot be empty')

    # Edit reply
    reply.update_content(comment)

def review_get_reply_wrapper(rid: str) -> dict[str, str]:
    '''
        Wrapper which grabs a review reply given an id
    '''
    # Grab reply
    reply = data_store.get_reply_by_id(rid)
    if reply is None:
        raise HTTPException(status_code=404, detail='Reply not found')
    
    return reply.to_json()