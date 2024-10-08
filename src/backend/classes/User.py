from typing import *

T = TypeVar("T")
K = TypeVar("K")

class User:

    '''
        Class representing a User on the platform

        Stores the following:

            uid:        ID of user
            username:   Username of user
            password:   Hashed password for security
            email:      Email registered with user
            icon_url:   Path to image store on backend (todo)
            role:       general | admin
            ---
            following:  List of services/users user is following
    
    '''

    def __init__(self,
                 uid: str,
                 username: str,
                 password: str,
                 email: str,
                 role: str,
                 icon_url: str = None) -> None:
        
        # Initialised vars
        self._id = uid
        self._name = username
        self._password = password
        self._email = email
        self._icon_url = icon_url
        self._role = role

        # Default vars
        self._following = []
        self._num_following = 0
    
    ################################
    #   Add Methods
    ################################
    def add_following(self, uid: str) -> None:
        '''
            Adds another user to list of users self is following
        '''
        self._following.append(uid)
        self._num_following += 1
    
    ################################
    #  Modify Methods
    ################################
    def modify_username(self, new: str) -> None:
        '''
            Modifies user's username
        '''
        self._name = new
    
    def modify_email(self, new: str) -> None:
        '''
            Modifies user's email
        '''
        self._email = new

    ################################
    #  Delete Methods
    ################################
    def remove_following(self, uid: str) -> None:
        '''
            Removes a user from self's following list
        '''
        self._following.remove(uid)
        self._num_following -= 1
    

    ################################
    #  Get Methods
    ################################
    def get_id(self) -> str:
        '''
            Returns uid of user
        '''
        return self._id
    
    def get_name(self) -> str:
        '''
            Returns username of user
        '''
        return self._name
    
    def get_email(self) -> str:
        '''
            Returns email of user
        '''
        return self._id
    
    def get_password(self) -> str:
        '''
            Return user password
        '''
        return self._password
    
    def get_icon_url(self) -> str:
        '''
            Return icon url of user
        '''
        return self._icon_url

    def get_following(self) -> str:
        '''
            Return list of users self is following
        '''
        return self._following
    
    def get_num_following(self) -> str:
        '''
            Return num of users self is following
        '''
        return self._num_following
    
    def get_role(self) -> List[str]:
        '''
            Return role of user
        '''
        return self._role
    
    ################################
    #  Storage Methods
    ################################
    def to_json(self) -> dict[T, K]:
        '''
            Converts object into json
        '''
        return {
            'id': self._id,
            'username' : self._name,
            'password' : self._password,
            'email' : self._email,
            'icon_url' : self._icon_url,
            'role' : self._role,
            'following' : self._following
        }