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
IMAGE_PATH = "static/imgs"
DOC_PATH = "static/docs"
MB1 = 1024 * 1024
IMAGE_TYPES = ["image/jpg", "image/jpeg", "image/png"]

async def upload_file(file: UploadFile, path: str) -> str:
    '''
        Helper function which uploads a given file to the given file path,
        returning the file path
    '''
    path_name = os.path.splitext(f"/{file.filename}")
    path_ext = f"{path_name[0]}_{data_store.num_docs()}{path_name[1]}"
    path += path_ext

    try:
        async with aiofiles.open(path, 'wb') as f:
            while contents := await file.read(MB1):
                await f.write(contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error with uploading file: {e}")
    
    finally:
        await file.close()
        await f.close()
    
    return path

async def upload_pdf_wrapper(file: UploadFile) -> str:
    '''
        Function which uploads pdf files
    '''
    path = DOC_PATH
    # Check type
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="File uploaded is not PDF")

    path = await upload_file(file, path)
    doc = Document(str(data_store.num_docs()), path, file.content_type)

    data_store.add_docs(doc)
    return str(doc.get_id())

async def upload_img_wrapper(file: UploadFile) -> int:
    '''
        Function which uploads image files
    '''
    path = IMAGE_PATH
    # Check type
    if file.content_type not in IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="File uploaded is not JPG, JPEG or PNG")

    path = await upload_file(file, path)
    doc = Document(str(data_store.num_docs()), path, file.content_type)

    data_store.add_docs(doc)
    return str(doc.get_id())