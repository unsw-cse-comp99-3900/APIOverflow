from pymongo import MongoClient
from typing import TypeVar, Optional
from dotenv import load_dotenv
import os

T = TypeVar("T")
K = TypeVar("K")

# load_dotenv()
# Initialize MongoDB client
# client = MongoClient("mongodb://mongodb:27017/", connect=False)

mongo_env = os.getenv('MONGO_ENV', 'local')

if mongo_env == 'docker':
    client = MongoClient("mongodb://mongodb:27017/", connect=False)
else:
    client = MongoClient("mongodb://localhost:27017/", connect=False)

global db
db = client.local

###################################
#       Adding Methods
###################################
def db_add_user(item: dict[T, K]) -> None:
    '''
        Adds a user into MongoDB
    '''
    db.users.insert_one(item)

def db_add_service(item: dict[T, K]) -> None:
    '''
        Adds a service into MongoDB
    '''
    db.services.insert_one(item)


###################################
#       Get Methods
###################################
def db_get_user(uid: str) -> dict[T, K] | None:
    '''
        Grabs user from MongoDB
    '''
    return db.users.find_one({"id": uid})

def db_get_service(sid: str) -> dict[T, K] | None:
    '''
        Grabs service from MongoDB
    '''
    return db.services.find_one({'id': sid})

###################################
#       Update (put) Methods
###################################

def db_update_user(uid: str, new_user: dict[T, K]) -> None:
    '''
        Update a mongodb user into MongoDB
    '''
    db.users.replace_one({"id": uid}, new_user)

def db_update_service(sid: str, updated_service_object: dict[T, K]) -> None:
    '''
        Update a service into MongoDB
    '''
    db.services.replace_one({'id': sid}, updated_service_object)

def db_add_document(sid: str, new_doc: int) -> None:
    old_documents = db_get_service(sid)["documents"]
    old_documents.append(new_doc)
    db.services.update_one({'id': sid}, {"$set": {'documents': old_documents}}, upsert=False)

###################################
#       Delete Methods
###################################

def clear_all_users() -> None:
    db.users.delete_many({})

def clear_all_services() -> None:
    db.services.delete_many({})
