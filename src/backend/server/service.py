from typing import TypeVar
from fastapi import APIRouter, HTTPException
from PIL import Image
import urllib.request
from urllib.error import HTTPError, URLError
from src.backend.classes.datastore import data_store
from src.backend.classes.API import API
from src.backend.database import *

IMAGE_PATH = "static"
T = TypeVar('T')
K = TypeVar('K')

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
                    [user],
                    internal_url,
                    packet['description'],
                    packet['tags'])

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
                    }
    '''

    # Error checking
    if sid == '':
        raise HTTPException(status_code=400, detail='No service id provided')

    service = data_store.get_api_by_id(sid)
    if service is None:
        raise HTTPException(status_code=404, detail='No service found with given sid')
    
    return {
            'sid' : service.get_id(),
            'name' : service.get_name(),
            'owner' : service.get_owner(),
            'description': service.get_description(),
            'icon_url': service.get_icon_url(),
            'tags' : service.get_tags()
    }
    
