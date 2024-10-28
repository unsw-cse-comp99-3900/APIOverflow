from typing import TypeVar, List, Union
from fastapi import File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from PIL import Image
import urllib.request
from urllib.error import HTTPError, URLError
from src.backend.classes.Service import ServiceStatus, LIVE_OPTIONS
from src.backend.classes.datastore import data_store
from src.backend.classes.API import API
from src.backend.database import *
from src.backend.classes.models import ServiceReviewInfo
from src.backend.classes.Review import Review, LIVE
import re


# Ollama information
OLLAMA_API_KEY = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBqE8KSc69XaJ4GwS37IXdk44ooXGidxNxeaKJNOUm4r'
OLLAMA_API_URL = 'http://<ip>:11434/api/generate'

# Constants
IMAGE_PATH = "static/imgs"
DOC_PATH = "static/docs"

T = TypeVar('T')
K = TypeVar('K')

# Helper functions

def validate_api_fields(packet: dict[T, K]) -> None:
    if packet['name'] == '':
        raise HTTPException(status_code=400, detail='No service name provided')
    
    if packet['description'] == '':
        raise HTTPException(status_code=400, detail='No service desc provided')
    
    if len(packet['tags']) == 0:
        raise HTTPException(status_code=400, detail='No service tags provided')
    
    if packet['endpoint'] == '':
        raise HTTPException(status_code=400, detail='No service endpoint provided')

def get_validate_service_id(sid: str) -> API:
    if sid == '':
        raise HTTPException(status_code=400, detail='No service id provided')

    service = data_store.get_api_by_id(sid)
    if service is None:
        raise HTTPException(status_code=404, detail='No service found with given sid')
    
    return service

# Endpoint Wrappers
def add_service_wrapper(packet: dict[T, K], user: str) -> dict[T, K]:
    '''
        Adds a Service (default to API) to the platform

        Raises:     HTTP Error 400 if missing info/bad request
        Returns:    sid representing id of newly created service
    '''
    validate_api_fields(packet)

    # Retrieve image from url
    response = None
    img_url = packet['icon_url']
    x_start, x_end = packet['x_start'], packet['x_end']
    y_start, y_end = packet['y_start'], packet['y_end']

    if x_start < 0 or y_start < 0 or x_start > x_end or y_start > y_end:
        raise HTTPException(status_code=400,
                            detail="Invalid X/Y dimensions")

    if img_url != '':
        internal_url = f"{IMAGE_PATH}/image{data_store.num_imgs()}.jpg"
        try:
            image, response = urllib.request.urlretrieve(img_url, internal_url)
        except HTTPError as err:
            raise HTTPException(status_code=400,
                                detail=f"HTTP exception {response} raised when retrieving image") from err
        except URLError as err:
            raise HTTPException(status_code=400,
                                detail=f"URL exception {response} raised when retrieving image") from err
        except Exception as err:
            raise HTTPException(status_code=400,
                                detail=f"An odd error {response} was raised when retrieving image") from err

        # Open image
        image_obj = Image.open(image)

        # Handle Error where x_start or y_start
        x_limit, y_limit = image_obj.size
        if x_end > x_limit or y_end > y_limit or x_start < 0 or y_start < 0:
            raise HTTPException(status_code=400,
                                detail="Boundaries for cropping beyond size of image")
        if x_start > x_end or y_start > y_end:
            raise HTTPException(status_code=400,
                                detail="X or Y start bigger than X/Y end")

        # Crop photo
        image_cropped = image_obj.crop((x_start, y_start, x_end, y_end))
        image_cropped.save(internal_url)

    else:
        internal_url = ""

    # Create new API
    new_api = API(str(data_store.num_apis()),
                    packet['name'],
                    user,
                    internal_url,
                    packet['description'],
                    packet['tags'],
                    packet['endpoint'])
    data_store.add_api(new_api)
    db_add_service(new_api.to_json())
    return str(new_api.get_id())

def update_service_wrapper(packet: dict[T, K], user: str) -> None:
    '''
        Updates a service by sid

        Raises:     HTTP Error 400 if missing info/bad request
                    HTTP Error 404 if no such sid found
        Returns:    None
    '''
    sid = packet["sid"]
    service = get_validate_service_id(sid)
    validate_api_fields(packet)

    # service is ref to API Obj in data store which gets updated
    service.create_pending_update(
        packet["name"], packet["description"], packet["tags"], packet["endpoint"])
    
    db_update_service(sid, service.to_json())
    return None

def get_service_wrapper(sid: str) -> dict[T : K]:
    '''
        Gets a service by sid

        Raises:     HTTP Error 400 if missing info/bad request
                    HTTP Error 404 if no such sid found
        Returns:    {
                        sid
                        name
                        owner
                        description
                        icon_url
                        tags
                        endpoint,
                        icon (doc_id)
                    }
    '''

    service = get_validate_service_id(sid)
    owner_id = service.get_owner()
    owner = data_store.get_user_by_id(owner_id)
    return {
            'id' : service.get_id(),
            'name' : service.get_name(),
            'owner' : {
                'id' : owner.get_id(),
                'name' : owner.get_name(),
                'email' : owner.get_email()
            },
            'description': service.get_description(),
            'icon_url': service.get_icon_url(),
            'tags' : service.get_tags(),
            'endpoint' : service.get_endpoint(),
            'docs' : service.get_docs(),
            'icon' : service.get_icon(),
            'status' : service.get_status().name,
            'status_reason' : service.get_status_reason()
    }
    
# function to match vincent's format, the one above is sid instead of id
def api_into_json(api) -> dict:
    return {
        'id': api.get_id(),
        'name': api.get_name(),
        'owner': api.get_owner(),
        'description': api.get_description(),
        'icon_url': api.get_icon_url(),
        'tags': api.get_tags()
    }

# filter through database to find APIs that are fitted to the selected tags
# returns a list of the filtered apis
def api_tag_filter(tags, providers, hide_pending: bool) -> list:

    api_list = data_store.get_apis()
    filtered_apis = []

    #query = input("Search")

    #if query != "":
        # if not empty, then Ollama match
    #    data = {
    #        "model": "llama3.2",
    #        "prompt": query
    #    }    
    #    response = requests.post(url, json=data)
        
    if not tags:
        # if they don't specify any tags, assume all APIs
        for api in api_list:
            filtered_apis.append(api)
    else:
        # otherwise get all the APIs with the tag/s
        for api in api_list:
            for tag in tags:
                if tag in api.get_tags() and api not in filtered_apis:
                        filtered_apis.append(api)

    return_list = []
    if providers:
        # if providers list is not empty
        for api in filtered_apis:
            for provider in providers:
                if provider in api.get_owner() and api not in return_list:
                    return_list.append(api)
                    break
    else:
        return_list = [api for api in filtered_apis]
    
    
    return [api_into_json(api) for api in return_list if
            api.get_status().name in LIVE_OPTIONS or 
            (not hide_pending and api.get_status() == ServiceStatus.PENDING)
            ]

# returns a list of regex matching services 
def api_name_search(name, hide_pending: bool) -> list: 
    api_list = data_store.get_apis()
    return_list = []
    for api in api_list:
        if re.search(name, api.get_name(), re.IGNORECASE) and (
            api.get_status().name in LIVE_OPTIONS or
            api.get_status() == ServiceStatus.PENDING and not hide_pending
        ):
            return_list.append(api)
    return return_list

async def upload_docs_wrapper(sid: str, uid: str, doc_id: str) -> None:
    '''
        Function which handles uploading docs to a service
    '''
    file = data_store.get_doc_by_id(doc_id)
    
    # Error Checks
    if file is None:
        raise HTTPException(status_code=400, detail="File not found")

    if file.get_type() != "application/pdf":
        raise HTTPException(status_code=400, detail="File is not a pdf")
    
    # Get service
    service = data_store.get_api_by_id(sid)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Check if user is owner
    if service.get_owner() != uid:
        raise HTTPException(status_code=403, detail="User is not service owner")

    # Add document to service
    service.add_docs([file.get_id()])
    db_add_document(sid, file.get_id())

def get_doc_wrapper(doc_id: str) -> FileResponse:
    '''
        Wrapper which returns the given file
    '''
    doc = data_store.get_doc_by_id(doc_id)
    if doc is None:
        raise HTTPException(status_code=404, detail="No such document found")
    
    return FileResponse(doc.get_path())

def list_pending_apis():
    return [api_into_json(api) for api in data_store.get_apis() if api.get_status() == ServiceStatus.PENDING]

def list_nonpending_apis():
    return [api_into_json(api) for api in data_store.get_apis() if api.get_status == ServiceStatus.LIVE]

def delete_service(sid: str):
    if sid == '':
        raise HTTPException(status_code=400, detail='No service id provided')

    service = data_store.get_api_by_id(sid)
    if service is None:
        raise HTTPException(status_code=404, detail='No service found with given sid')
    service_name = service.get_name()
    data_store.delete_item(sid, 'api')
    db_status = db_delete_service(service_name)

    return {"name": service_name, "deleted": db_status}

def service_add_icon_wrapper(uid: str, sid: str, doc_id: str) -> None:
    '''
        Wrapper which handles adding an icon to a service
    '''

    # Grab user
    user = data_store.get_user_by_id(uid)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    # Grab service
    service = data_store.get_api_by_id(sid)
    if service is None:
        raise HTTPException(status_code=404, detail='Service not found')
    
    # Grab icon
    icon = data_store.get_doc_by_id(doc_id)
    if icon is None:
        raise HTTPException(status_code=404, detail='Icon not found')

    # Check whether user is allowed to modify icon
    if service.get_owner() != user.get_id():
        raise HTTPException(status_code=403, detail='User not service owner')

    service.update_icon_id(doc_id)

def service_delete_icon_wrapper(uid: str, sid: str) -> None:
    '''
        Wrapper which handles deleting an icon to a service
    '''

    # Grab user
    user = data_store.get_user_by_id(uid)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    
    # Grab service
    service = data_store.get_api_by_id(sid)
    if service is None:
        raise HTTPException(status_code=404, detail='Service not found')
    
    # Check whether user is allowed to modify icon
    if service.get_owner() != user.get_id():
        raise HTTPException(status_code=403, detail='User not service owner')

    service.remove_icon()

def service_get_icon_wrapper(sid: str) -> FileResponse:
    '''
        Wrapper which returns image file of service's icon
    '''
    # Grab service
    service = data_store.get_api_by_id(sid)
    if service is None:
        raise HTTPException(status_code=404, detail='Service not found')

    # Grab image file
    icon_id = service.get_icon()
    icon = data_store.get_doc_by_id(icon_id)
    return FileResponse(icon.get_path())

def service_add_review_wrapper(uid: str, info: ServiceReviewInfo):
    '''
        Wrapper which adds a review to a service
    '''
    data = info.model_dump()

    # Grab server
    sid = data['sid']
    service = data_store.get_api_by_id(sid)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Grab User
    user = data_store.get_user_by_id(uid)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check whether user attempting to review their own service
    if service.get_owner() == user.get_id():
         raise HTTPException(status_code=403, detail="Cannot review own service")

    # Check whether user has already reviewed this service
    for review in service.get_reviews():
        if review in user.get_reviews():
            raise HTTPException(status_code=403, detail="User already reviewed!")

    # Validate Review
    rating = data['rating']
    title = data['title']
    comment = data['comment']
    if rating == '' or title == '' or comment == '':
         raise HTTPException(status_code=400, detail="Rating/Title/Comment is empty")

    if rating not in ['positive', 'negative']:
         raise HTTPException(status_code=400, detail="Invalid rating given")

    # Create and add review
    review = Review(str(data_store.total_reviews()),
                    user.get_id(),
                    service.get_id(),
                    title,
                    rating,
                    comment)
    data_store.add_review(review)
    service.add_review(review.get_id(), rating)
    user.add_review(review.get_id())

def service_get_rating_wrapper(sid: str) -> dict[str, Union[int, float]]:
    '''
        Wrapper which gets the rating of an existing service
    '''
    # Grab server
    service = data_store.get_api_by_id(sid)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    return service.get_ratings()

def service_get_reviews_wrapper(sid: str, testing: bool = False) -> List[dict[str, str]]:
    '''
        Wrapper which grabs all reviews associated with the particular service
    '''
    # Grab server
    service = data_store.get_api_by_id(sid)
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Grab reviews
    reviews = []
    for rid in service.get_reviews():
        review = data_store.get_review_by_id(rid)
        
        # This should not trigger, but is there just in case
        if review is None:
            continue

        # Ensure only live reviews are shown
        if review.get_status() != LIVE and not testing:
            continue

        reviews.append(review.to_json())

    return reviews

def approve_service_wrapper(sid: str, approved: bool, reason: str):

    service = data_store.get_api_by_id(sid)

    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    
    if approved:
        service.complete_update()
        service.update_status(ServiceStatus.LIVE, reason)
        db_update_service(sid, service.to_json())
    elif service.get_status() == ServiceStatus.PENDING:
        service.update_status(ServiceStatus.REJECTED, reason)
    elif service.get_status() == ServiceStatus.UPDATE_PENDING:
        service.update_status(ServiceStatus.UPDATE_REJECTED, reason)
        
