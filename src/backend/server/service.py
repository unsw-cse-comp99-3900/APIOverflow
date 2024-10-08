from typing import TypeVar
from fastapi import File, UploadFile, HTTPException
from PIL import Image
import urllib.request
from urllib.error import HTTPError, URLError
from src.backend.classes.datastore import data_store
from src.backend.classes.API import API
from src.backend.database import *
from src.backend.server.upload import upload_wrapper

# Constants
IMAGE_PATH = "static/imgs"
DOC_PATH = "static/docs"
T = TypeVar('T')
K = TypeVar('K')

# Helper functions

# Endpoint Wrappers
def add_service_wrapper(packet: dict[T, K], user: str) -> dict[T, K]:
    '''
        Adds a Service (default to API) to the platform

        Raises:     HTTP Error 400 if missing info/bad request
        Returns:    sid representing id of newly created service
    '''

    # Error Checking
    if packet['name'] == '':
        raise HTTPException(status_code=400, detail='No service name provided')
    
    if packet['description'] == '':
        raise HTTPException(status_code=400, detail='No service desc provided')
    
    if len(packet['tags']) == 0:
        raise HTTPException(status_code=400, detail='No service tags provided')
    
    if packet['endpoint'] == '':
        raise HTTPException(status_code=400, detail='No service endpoint provided')

    # Retrieve image from url
    response = None
    img_url = packet['icon_url']
    x_start, x_end = packet['x_start'], packet['x_end']
    y_start, y_end = packet['y_start'], packet['y_end']

    if x_start < 0 or y_start < 0 or x_start > x_end or y_start > y_end:
        raise HTTPException(status_code=400,
                            detail="Invalid X/Y dimensions")

    # Handle custom image
    # TODO
    #   Shrink images instead of cropping
    #   Impose some sort of icon limit 

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
        internal_url = f"{IMAGE_PATH}/default_icon2.png"


    # Create new API
    new_api = API(  str(data_store.num_apis()),
                    packet['name'],
                    user,
                    internal_url,
                    packet['description'],
                    packet['tags'],
                    packet['endpoint'])

    data_store.add_api(new_api)
    db_add_service(new_api.to_json())
    return str(new_api.get_id())

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
                        endpoint
                    }
    '''

    # Error checking
    if sid == '':
        raise HTTPException(status_code=400, detail='No service id provided')

    service = data_store.get_api_by_id(sid)
    if service is None:
        raise HTTPException(status_code=404, detail='No service found with given sid')
    
    owner_id = service.get_owner()
    owner = data_store.get_user_by_id(owner_id)
    doc_ids = service.get_docs()
    docs = [data_store.get_doc_by_id(i) for i in doc_ids]
    doc_paths = [i.get_path() for i in docs]
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
            'docs' : doc_paths
    }
    
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
