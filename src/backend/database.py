from pymongo import MongoClient
from typing import TypeVar, Optional

T = TypeVar("T")
K = TypeVar("K")

# Initialize MongoDB client
client = MongoClient("mongodb://mongodb:27017/")

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