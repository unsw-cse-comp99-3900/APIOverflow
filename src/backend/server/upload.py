from typing import TypeVar
from fastapi import APIRouter, HTTPException, File, UploadFile
from PIL import Image
import urllib.request
from urllib.error import HTTPError, URLError
from src.backend.classes.datastore import data_store
from src.backend.classes.API import API
from src.backend.classes.Document import Document
from src.backend.database import *
import aiofiles
import os

# Constants
IMAGE_PATH = "src/backend/static/imgs"
DOC_PATH = "src/backend/static/docs"
MB1 = 1024 * 1024

async def upload_wrapper(file: UploadFile) -> str:
    '''
        Function which uploads files into specified path
    '''
    # Check type
    if file.content_type == 'application/pdf':
        path = DOC_PATH
    else:
        path = IMAGE_PATH

    path_ext = os.path.splitext(f"/{file.filename}")[0] + f"_{data_store.num_docs()}.pdf"
    path += path_ext

    try:
        async with aiofiles.open(path, 'wb') as f:
            while contents := await file.read(MB1):
                await f.write(contents)
    except Exception:
        raise HTTPException(status_code=400, detail="Error with uploading file")
    
    finally:
        await file.close()

    doc = Document(str(data_store.num_docs()), path, file.content_type)
    data_store.add_docs(doc)
    return doc.get_id()
