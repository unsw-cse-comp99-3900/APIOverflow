from typing import *

T = TypeVar("T")
K = TypeVar("K")

class Service:

    '''
    Abstract class Service which encapsulates the properties shared between
    'API' and 'Microservice' 

    Stores the following:
        sid:            ID of service
        name:           Name of the service
        owner:          For now, only one owner
        icon_url:       Path to image store on backend
        description:    User-given description of service
        tags:           List of tags given to service
        endpoint:       Endpoint of the service
        
        ----
        owner_count:    Number of owners for this service
        documents:      List of paths to documents uploaded by user re service
        doc_count:      Number of documents uploaded to service
        users:          List of users using/subscribed to service
        user_count:     Number of users using/subscribing to service
        reviews:        List of reviews given by users
        review_count:   Number of reviews the service has
        upvotes:        Number of upvotes given to service
        type:           Type of service ['api', 'micro']

    '''

    def __init__(self,
                 sid: str,
                 name: str,
                 owner: str,
                 icon_url: str,
                 description: str,
                 tags: List[str],
                 endpoint: str,
                 stype: str) -> None:
        
        # Initialised vars
        self._id = sid
        self._name = name
        self._owner = owner
        self._owner_count = 1
        self._icon_url= icon_url
        self._description = description
        self._tags = tags
        self._endpoint = endpoint
        self._type = stype

        # Default vars
        self._docs = []
        self._doc_count = 0
        self._users = []
        self._user_count = 0
        self._reviews = []
        self._review_count = 0
        self._upvotes = 0
    
    ################################
    #   Add Methods
    ################################

    def add_docs(self, docs: List[int]) -> None:
        '''
            Adds paths to documentation
        '''
        for doc in docs:
            self._docs.append(doc)
            self._doc_count += 1

    def add_user(self, uid: str) -> None:
        '''
            Adds user to subscription/usage list
        '''
        self._users.append(uid)
        self._user_count += 1

    def add_review(self, review: T) -> None:
        '''
            Adds review to service
        '''
        self._reviews.append(review)
        self._review_count += 1
   
    def add_upvote(self) -> None:
        '''
            Adds upvote to service
        '''
        self._upvotes += 1

    def add_tag(self, tag) -> None:
        '''
            Adds tag to service
        '''
        self._tags.append(tag)

    # def add_owner(self, owner: str) -> None:
    #     '''
    #         Adds owner to service
    #     '''
    #     self._owner.append(owner)
    #     self._owner_count += 1
    
    ################################
    #   Update Methods
    ################################

    def update_name(self, name: str) -> None:
        '''
            Update service name
        '''
        self._name = name
    
    def update_icon(self, url: str) -> None:
        '''
            Update service icon
        '''
        self._icon_url = url

    def update_description(self, desc: str) -> None:
        '''
            Update service description
        '''
        self._description = desc

    ################################
    #   Delete Methods
    ################################
    def remove_doc(self, doc: str) -> None:
        '''
            Remove path to documentation
        '''
        self._docs.remove(doc)
        self._doc_count -= 1

    def remove_user(self, uid: str) -> None:
        '''
            Removes user from subscription/usage list
        '''
        self._users.remove(uid)
        self._user_count -= 1

    def remove_review(self, review: T) -> None:
        '''
            Removes review from service
        '''
        self._reviews.remove(review)
        self._review_count -= 1
   
    def remove_upvote(self) -> None:
        '''
            Removes upvote from service
        '''
        self._upvotes -= 1

    def remove_tag(self, tag) -> None:
        '''
            Removes tag from service
        '''
        self._tags.remove(tag)

    # def remove_owner(self, uid: str) -> None:
    #     '''
    #         Remove owner from ownership list
    #     '''
    #     self._owner.remove(uid)
    #     self._owner_count -= 1

    ################################
    #   Get Methods
    ################################
    def get_id(self) -> str:
        '''
            Returns sid of service
        '''
        return self._id
    
    def get_name(self) -> str:
        '''
            Returns name of service
        '''
        return self._name
    
    def get_description(self) -> str:
        '''
            Returns description of service
        '''
        return self._description
    
    def get_owner(self) -> str:
        '''
            Returns description of service
        '''
        return self._owner

    def get_tags(self) -> List[str]:
        '''
            Returns tags of service
        '''
        return self._tags
    
    def get_icon_url(self) -> str:
        '''
            Returns icon_url of service
        '''
        return self._icon_url
    
    def get_endpoint(self) -> str:
        '''
            Returns endpoint of service
        '''
        return self._endpoint
    
    def get_docs(self) -> List[str]:
        '''
            Returns icon_url of service
        '''
        return self._docs

    ################################
    #  Storage Methods
    ################################
    def to_json(self) -> dict[T, K]:
        '''
            Converts object into json
        '''
        return {
            'id': self._id,
            'name' : self._name,
            'owner' : self._owner,
            'icon_url' : self._icon_url,
            'description' : self._description,
            'tags' : self._tags,
            'endpoint': self._endpoint,
            'documents' : self._docs,
            'users' : self._users,
            'reviews': self._reviews,
            'upvotes': self._upvotes,
            'type': self._type
        }
