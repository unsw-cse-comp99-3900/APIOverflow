from fastapi import HTTPException
from src.backend.classes.datastore import data_store, defaults
import requests
import json
from src.backend.classes.Tag import SYSTEM, CUSTOM

vm_ip = "34.116.117.133"
url = f"http://{vm_ip}:11434/api/generate"

n_tags_max = 10
n_tags_min = 1
def auto_generate_tags(description: str):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "llama3:latest",
        "prompt": f"Generate exactly betwen {n_tags_min} to {n_tags_max} concise tags for the following text (depending how descriptive the text is). Provide the tags only as a comma-separated list, with no additional text or explanation. Here's the text: {description}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), stream=False)

    if response.status_code == 200:
        final_response = ""
        for line in response.iter_lines():
            if line:
                json_line = json.loads(line.decode('utf-8'))
                if 'response' in json_line:
                    final_response += json_line['response']
                if json_line.get('done'):
                    break
        tag_list = [tag.strip() for tag in final_response.split(',')]
        return tag_list
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

def add_tag_wrapper(tag: str):
    '''
        Wrapper function which adds a tag to the data_store
    '''
    if tag == '':
        raise HTTPException(status_code=400, detail="Empty tag given")
    
    if data_store.add_tag(tag) is None:
        raise HTTPException(status_code=400, detail="Duplicate tag given")

def get_tags_wrapper(_system: bool = False):
    '''
        Wrapper function which grabs all tags stored in the data_store
    
    '''
    if _system:
        return {'tags' : [tag.get_tag() for tag in data_store.get_tags() if tag.get_type() == SYSTEM]}

    return {'tags' : [tag.get_tag() for tag in data_store.get_tags()]}

def delete_tag_wrapper(tag: str):
    '''
        Wrapper function which deletes a tag from the data_store
    '''

    if tag in defaults:
        raise HTTPException(status_code=400, detail="Attempted to delete system tag")

    if data_store.delete_tag(tag) is None:
        raise HTTPException(status_code=404, detail="Tag not found")

def get_top_tags_wrapper(num: int, custom: bool = False):
    '''
        Wrapper function which grabs the top 'num' tags
    '''
    return data_store.get_tag_ranking(num, custom)