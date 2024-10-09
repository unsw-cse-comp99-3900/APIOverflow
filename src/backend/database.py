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
def db_get_user(username: str) -> dict[T, K] | None:
    '''
        Grabs user from MongoDB
    '''
    return db.users.find_one({"username": username})

def db_get_service(name: str) -> dict[T, K] | None:
    '''
        Grabs service from MongoDB
    '''
    return db.services.find_one({'name': name})

###################################
#       Update (put) Methods
###################################
def db_update_user(username: str, new_user: dict[T, K]) -> None:
    '''
        Update a mongodb user into MongoDB
    '''
    db.users.replace_one({"username": username}, new_user)

def db_update_service(service_name: str, new_service: dict[T, K]) -> None:
    '''
        Update a service into MongoDB
    '''
    db.services.replace_one({'name': service_name}, new_service)

###################################
#       Delete Methods
###################################

def clear_all_users() -> None:
    db.users.delete_many({})

def clear_all_services() -> None:
    db.services.delete_many({})

def db_delete_service(name: str) -> None:
    """
    Deletes a service from MongoDB by its service_name.
    """
    db.services.delete_one({'name': name})
    return True
