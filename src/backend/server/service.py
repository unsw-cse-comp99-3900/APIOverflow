from typing import TypeVar
from fastapi import APIRouter, HTTPException
from PIL import Image
from typing import List
import urllib.request
from urllib.error import HTTPError, URLError
from src.backend.classes.datastore import data_store
from src.backend.classes.API import API
from flask import Flask, request, jsonify

app = Flask(__name__)

# Ollama information
OLLAMA_API_KEY = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBqE8KSc69XaJ4GwS37IXdk44ooXGidxNxeaKJNOUm4r'
OLLAMA_API_URL = 'http://<ip>:11434/api/generate'

IMAGE_PATH = "src/backend/static"
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
    if service == None:
        raise HTTPException(status_code=404, detail='No service found with given sid')
    
    return {
            'sid' : service.get_id(),
            'name' : service.get_name(),
            'owner' : service.get_owner(),
            'description': service.get_description(),
            'icon_url': service.get_icon_url(),
            'tags' : service.get_tags()
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
def api_tag_filter(tags, providers) -> List:

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
        
    if len(tags) == 0:
        # if they don't specify any tags, assume all APIs
        for api in api_list:

            filtered_apis.append(api)
    else:
        # otherwise get all the APIs with the tag/s
        for api in api_list:
            for tag in tags:
                if tag in api.tags:
                    filtered_apis.append(api)
    
    if len(providers) != 0:
        # if providers list is not empty
        for api in filtered_apis:
            for provider in providers:
                if provider in api.owners:
                    break
                # if we've reached here that means none of the providers specified
                # were in the owners list. therefore, filter it
                filtered_apis.remove(api)

    # list of JSON objects
    return_list = []
    for api in filtered_apis:
        return_list.append(jsonify(api_into_json(api)))
    return filtered_apis

def list_apis():
    api_list = data_store.get_apis()
    return_list = []
    for api in api_list:
        return_list.append(jsonify(api_into_json(api)))
    return return_list