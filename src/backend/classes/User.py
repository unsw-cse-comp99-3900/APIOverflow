from typing import *

T = TypeVar("T")
K = TypeVar("K")

DEFAULT_ICON = '0'

class User:

    '''
        Class representing a User on the platform

        Stores the following:

            uid:        ID of user
            username:   Username of user
            password:   Hashed password for security
            email:      Email registered with user
            icon_url:   Path to image store on backend (todo)
            is_admin:   Is the user an admin
            is_super:   Is the user a super admin
            icon:       ID of image file serving as user's icon
            ---
            following:  List of services/users user is following
            reviews:    List of reviews the user has posted
    
    '''

    def __init__(self,
                 uid: str,
                 username: str,
                 password: str,
                 email: str,
                 is_admin: bool,
                 is_super: bool,
                 icon_url: str = None) -> None:
        
        # Initialised vars
        self._id = uid
        self._name = username
        self._password = password
        self._email = email
        self._icon_url = icon_url
        self._is_admin = is_admin
        self._is_super = is_super

        # Default vars
        self._following = []
        self._num_following = 0
        self._icon = DEFAULT_ICON
        self._is_verified = False
        self._reviews = []
        self._num_reviews = 0
    
    ################################
    #   Add Methods
    ################################
    def add_following(self, uid: str) -> None:
        '''
            Adds another user to list of users self is following
        '''
        self._following.append(uid)
        self._num_following += 1

    def add_review(self, rid: str) -> None:
        '''
            Adds a review to the user's list
        '''
        self._reviews.append(rid)
        self._num_reviews += 1

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
    
    def promote_to_admin(self) -> None:
        '''
            Promotes user to admin
        '''
        self._is_admin = True

    def demote_to_user(self) -> None:
        '''
            Demotes user from admin
        '''
        self._is_admin = False

    def modify_icon(self, doc_id: str) -> None:
        '''
            Modifies user's icon
        '''
        self._icon = doc_id

    def verify_user(self) -> None:
        '''
            Verify the user
        '''
        self._is_verified = True

    def change_password(self, new:str) -> None:
        '''
            Changes the user password
        '''
        self._password = new

    ################################
    #  Delete Methods
    ################################
    def remove_following(self, uid: str) -> None:
        '''
            Removes a user from self's following list
        '''
        self._following.remove(uid)
        self._num_following -= 1
    
    def remove_icon(self) -> None:
        '''
            Removes user's current icon
        '''
        self._icon = DEFAULT_ICON

    def remove_review(self, rid: str) -> None:
        '''
            Removes a review from the user's list
        '''
        self._reviews.remove(rid)
        self._num_reviews -= 1

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
        return self._email
    
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
    
    def get_is_admin(self) -> bool:
        '''
            Return the admin status of the user
        '''
        return self._is_admin
    
    def get_is_super(self) -> bool:
        '''
            Return the super admin status of the user
        '''
        return self._is_super
    
    def get_icon(self) -> str:
        '''
            Grabs user's icon (in doc_id form)
        '''
        return self._icon

    def get_is_verified(self) -> bool:
        '''
            Return the verify status of the user
        '''
        return self._is_verified
    
    def get_reviews(self) -> List[str]:
        '''
            Return list of reviews
        '''
        return self._reviews
    
    def get_profile(self) -> dict[str, str]:
        '''
            Returns profile info of user
        '''
        return {
            'email': self._email,
            'username': self._name,
            'icon': self._icon
        }

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
            'is_admin' : self._is_admin,
            'is_super' : self._is_super,
            'following' : self._following,
            'is_verified': self._is_verified,
            'reviews': self._reviews,
            'icon' : self._icon
        }