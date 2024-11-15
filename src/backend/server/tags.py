from fastapi import HTTPException
from src.backend.classes.datastore import data_store, defaults

def add_tag_wrapper(tag: str):
    '''
        Wrapper function which adds a tag to the data_store
    '''
    if tag == '':
        raise HTTPException(status_code=400, detail="Empty tag given")
    
    if data_store.add_tag(tag) is None:
        raise HTTPException(status_code=400, detail="Duplicate tag given")

def get_tags_wrapper():
    '''
        Wrapper function which grabs all tags stored in the data_store
    
    '''
    return {'tags' : [tag.get_tag() for tag in data_store.get_tags()]}

def delete_tag_wrapper(tag: str):
    '''
        Wrapper function which deletes a tag from the data_store
    '''

    if tag in defaults:
        raise HTTPException(status_code=400, detail="Attempted to delete system tag")

    if data_store.delete_tag(tag) is None:
        raise HTTPException(status_code=404, detail="Tag not found")
