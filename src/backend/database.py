from pymongo import MongoClient
from typing import TypeVar, Optional

T = TypeVar("T")
K = TypeVar("K")

# Initialize MongoDB client
client = MongoClient("mongodb://localhost:27017/")

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
def db_get_user(username: str) -> Optional[dict]:
    '''
        Grabs user from MongoDB
    '''
    return db.users.find_one({"username": username})

def db_get_service(name: str) -> Optional[dict]:
    '''
        Grabs service from MongoDB
    '''
    return db.services.find_one({'service_name': name})


###################################
#       Update (put) Methods
###################################
def db_update_user(username: str, new_user: dict[T, K]) -> None:
    '''
        Update a mongodb user into MongoDB
    '''
    db.users.update_one({"username": username}, new_user)

def db_update_service(service_name: str, new_service: dict[T, K]) -> None:
    '''
        Update a service into MongoDB
    '''
    db.services.update_one({'service_name': service_name}, new_service)

