from fastapi import APIRouter, HTTPException, status, Depends
from fastapi_login import LoginManager
from pydantic import BaseModel
from passlib.context import CryptContext
from src.backend.classes.datastore import data_store
from src.backend.database import *
from datetime import timedelta

TOKEN_DURATION = timedelta(days=1)     # 1 day expiration

class Manager:
    '''
        Class which handles session-management and password security
    '''

    def __init__(self, manager: LoginManager, pwd_context = CryptContext) -> None:
        
        self._manager = manager
        self._pwd_context = pwd_context
    
    ################################
    #   Get Methods
    ################################
    def get_manager(self) -> LoginManager:
        '''
            Returns manager
        '''
        return self._manager
    
    ################################
    #   Session / Password Methods
    ################################

    def hash_password(self, password: str) -> str:
        '''
            Hashes given password with pwd_context
        '''
        return self._pwd_context.hash(password)

    def verify_password(self, password_given: str, password_compare) -> bool:
        '''
            Verifies given password with comparison password
        '''
        return self._pwd_context.verify(password_given, password_compare)

    def create_access_token(self, data : dict[T, K]) -> str:
        '''
            Creates a session token with encoded data
        '''
        return self._manager.create_access_token(data=data, expires=TOKEN_DURATION)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET = 'supersecretkey'
_manager = LoginManager(SECRET, token_url='/auth/login')

@_manager.user_loader()
def load_user(username: str):
    '''
        Grabs user for manager
    '''
    user = data_store.get_user_by_id(username)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    user_body = {
        'id' : user.get_id(),
        'username' : user.get_name(),
        'email' : user.get_email(),
        'password' : user.get_password(),
        'is_admin' : user.get_is_admin(),
        'is_super' : user.get_is_super(),
    }
    return user_body

global manager
manager = Manager(_manager, pwd_context)
