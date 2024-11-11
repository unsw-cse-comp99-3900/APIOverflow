from typing import *
from enum import Enum
from src.backend.classes.Endpoint import Endpoint
from src.backend.classes.Document import Document
from src.backend.classes.User import User

from fastapi import HTTPException

class ServiceStatus(Enum):
    UPDATE_REJECTED = 3
    UPDATE_PENDING = 2
    LIVE = 1
    PENDING = 0
    REJECTED = -1

STATUS_STRINGS = ["LIVE", "PENDING", "REJECTED", "UPDATE_PENDING", "UPDATE_REJECTED"]
STATUS_OPTIONS = ["LIVE", "PENDING", "REJECTED", "UPDATE_PENDING", "UPDATE_REJECTED", "ALL", "ALL_PENDING"]
PENDING_OPTIONS = ["PENDING", "UPDATE_PENDING"]
LIVE_OPTIONS = ["LIVE", "UPDATE_PENDING", "UPDATE_REJECTED"]

T = TypeVar("T")
K = TypeVar("K")
DEFAULT_ICON = '0'

# API Changes
# /service/add: added "version_name" and "version_description" fields
#  - currently these give a default value to break existing things
#  - but pls change so users must provide these strings
#
# /service/get: 
#  - REMOVED FIELDS endpoints and docs
#  - Added field: versions: [{
            # "version_name": name of version(str)
            # "endpoints": list of endpoints (whatever it was before),
            # "version_description": Additional description for version(str),
            # "docs": documents (whatever it was before)
            # "status": name of status: 
            # "status_reason": self._status_reason
# }]
# - It is important that FE does NOT display
# - a status version if status == "PENDING" or "REJECTED"
# - it should still display for UPDATE_PENDING and UPDATE_REJECTED
# - since the pre-updated version should still be live
#
# /service/update: No longer contains endpoints field (only updates global fields)

#    
# for simplicity / to avoid a bunch of funky edge cases, we can only perform
# one update at once, adding a new version is considered an update
# trying to make second update will automatically ovewrite first

# Added Endpoints:
# /service/version/add : POST
# Fields:
#  - sid: str                        # id of service 
#  - version_name: str               # name of new version
#  - endpoints: List[Endpoint]       # endpoints of new version
#  - version_description: str        # Additional details pertaining new version   



# TODOs
# 5. Delete service version
# 7. Updating a Service 
# [X] existing update API no longer updates endpoint
# -- create new endpoint for updating specific version
# -- get pending returns more stuff
# -- approve service must return a version as well, omitting field indicates global
# -- create new  service version approval
# -- a) remove endpoint from service update
# -- b) create new endpoint 
# 6. Add docs now requires a version name
#     - currently only supports 1 doc, should it support more?
#     - currently cannot delete a doc  
# Consider problem of both global and local pending upon new creation


class ServiceVersionInfo:
    '''
        Information about a service which is version specific

        version_name:  name of version
        endpoints: list of endpoints
        version_description: additional version specific details
        documents: List of documents
    '''

    def __init__(self,
                 version_name: str,
                 endpoints: List[Endpoint],
                 version_description: str):
        self._version_name: str = version_name
        self._endpoints: List[Endpoint] = endpoints
        self._version_description: str = version_description
        
        self._docs: List[Document] = []
        self._pending_update: Optional[ServicePendingVersionUpdate] = None
        self._status : ServiceStatus = ServiceStatus.PENDING
        self._status_reason : str = ""




    def to_json(self):
        return {
            "version_name": self._version_name,
            "endpoints": self._endpoints,
            "version_description": self._version_description,
            "docs": self._docs,
            "status": self._status.name,
            "status_reason": self._status_reason

        }
    
    def to_updated_json(self):
        pass
    
    def update_status(self, status: ServiceStatus, reason: str):
        self._status = status
        self._status_reason = reason
    
    def get_status(self):
        return self._status
    
    def create_pending_update(self,
            version_name: str,
            endpoints: List[Endpoint],
            version_description: str
            ):
    
        self.update_status(ServiceStatus.UPDATE_PENDING, "")
        self._pending_update = ServicePendingVersionUpdate(version_name, endpoints, version_description)
    
    def complete_update(self):
        if self._status == ServiceStatus.UPDATE_PENDING:
            self._version_name = self._pending_update._version_name
            self._endpoints = self._pending_update._endpoints
            self._version_description = self._pending_update._version_description

            self._pending_update = None
        



class ServicePendingVersionUpdate:
    '''
        stores the updates related to a specific version of a service
    '''
    def __init__(self,
                 version_name: str,
                 endpoints: List[Endpoint],
                 version_description: str):
        self._version_name: str = version_name
        self._endpoints: List[Endpoint] = endpoints
        self._version_description: str = version_description

    def get_version_name(self) -> str:
        return self._version_name
    
    def get_endpoints(self) -> List[Endpoint]:
        return self._endpoints
    
    def get_version_description(self) -> str:
        return self._version_description

class ServicePendingGlobalUpdate:
    '''
        Stores the updates related to the global fields of a service
    '''

    def __init__(self,
                 name: str,
                 description: str, 
                 tags: List[str]
                 ):
        
        # these fields don't require a version to update
        self._name = name
        self._description = description
        self._tags = tags

    def get_name(self) -> str:
        return self._name
    
    def get_description(self) -> str:
        return self._description
    
    def get_tags(self) -> List[str]:
        return self._tags
    


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
        endpoints:       List of Endpoint of the service
        
        ----
        version_info    List of all versions of service, with most recently created first
        icon            Doc_ID of service icon. Has a default icon
        owner_count:    Number of owners for this service
        documents:      List of paths to documents uploaded by user re service
        doc_count:      Number of documents uploaded to service
        users:          List of users using/subscribed to service
        user_count:     Number of users using/subscribing to service
        reviews:        List of reviews given by users
        review_count:   Number of reviews the service has
        upvotes:        Number of upvotes given to service
        downvotes:      Number of downvotes given to service
        type:           Type of service ['api', 'micro']
        status:         Status of service [LIVE, PENDING, REJECTED]
        status_reason:  Reason for status
        reviews:        List of reviews (rid)
        pending_update:  Pending update Details when waiting to approve an update

    '''

    def __init__(self,
                 sid: str,
                 name: str,
                 owner: User,
                 icon_url: str,
                 description: str,
                 tags: List[str],
                 endpoints: List[Endpoint],
                 stype: str,
                 version_name: str,
                 version_description: str,
                 icon: str = DEFAULT_ICON) -> None:
        
        # Initialised vars
        self._id = sid
        self._name = name
        self._owner = owner
        self._owner_count = 1
        self._icon_url= icon_url
        self._description = description
        self._tags = tags
        self._type = stype
        self._version_info : List[ServiceVersionInfo] = []
        self.add_service_version(version_name, endpoints, version_description)

        # Default vars
        self._users = []
        self._user_count = 0
        self._reviews = []
        self._review_count = 0
        self._upvotes = 0
        self._downvotes = 0
        self._pending_update = None

        self._status = ServiceStatus.PENDING
        self._status_reason = ""
        self._icon = icon
    
    ################################
    #   Add Methods
    ################################

    def add_docs(self, docs: List[int], version: Optional[str] = None) -> None:
        '''
            Adds paths to documentation
        '''
        version: ServiceVersionInfo = self.get_version_info(version)
        for doc in docs:
            version._docs.append(doc)
    def add_user(self, uid: str) -> None:
        '''
            Adds user to subscription/usage list
        '''
        self._users.append(uid)
        self._user_count += 1

    def add_review(self, review: str, rating: str) -> None:
        '''
            Adds review to service
        '''
        self._reviews.append(review)
        self._review_count += 1
    
        if rating == 'positive':
            self._upvotes += 1
        else:
            self._downvotes += 1

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

    def add_endpoint(self, tab, parameters, method, version: Optional[str] = None) -> None:
        '''
            Adds an endpoint to the service
        '''
        
        new_endpoint = Endpoint(tab, parameters, method)
        self.get_version_info(version)._endpoints.append(new_endpoint)
    
    def add_service_version(self, version_name: str, endpoints: List[Endpoint], version_description: str):
        if version_name == "":
            raise HTTPException(status_code=400, detail='Version name cannot be empty')

        if any(version._version_name == version_name for version in self._version_info):
            raise HTTPException(status_code=404, detail='Version names must be Unique')
        
        # maintain version_info has most recently added version at front of list
        self._version_info.insert(0,
            ServiceVersionInfo(version_name, endpoints, version_description)
        )
        


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

    def update_icon_id(self, icon_id: str) -> None:
        '''
            Update service icon
        '''
        self._icon = icon_id
    
    def update_status(self, status: ServiceStatus, reason: str):
        self._status = status
        self._status_reason = reason
    
    def create_pending_update(self,
                name: str,
                description: str,
                tags: List[str]
                ):
        
        self.update_status(ServiceStatus.UPDATE_PENDING, "")

        self._pending_update = ServicePendingGlobalUpdate(name, description, tags)
    
    def complete_update(self):
        if self._status == ServiceStatus.UPDATE_PENDING:
            self._name = self._pending_update.get_name()
            self._description = self._pending_update.get_description()
            self._tags = self._pending_update.get_tags()

            self._pending_update = None

    ################################
    #   Delete Methods
    ################################
    def remove_doc(self, doc: str, version: Optional[str] = None) -> None:
        '''
            Remove path to documentation
        '''

        self.get_version_info(version)._docs.remove(doc)

    def remove_user(self, uid: str) -> None:
        '''
            Removes user from subscription/usage list
        '''
        self._users.remove(uid)
        self._user_count -= 1

    def remove_review(self, review: str, rating: str) -> None:
        '''
            Removes review from service
        '''
        self._reviews.remove(review)
        self._review_count -= 1

        if rating == 'positive':
            self._upvotes -= 1
        else:
            self._downvotes -= 1
   
    def remove_tag(self, tag) -> None:
        '''
            Removes tag from service
        '''
        self._tags.remove(tag)

    def remove_icon(self) -> None:
        '''
            Removes icon from service and restores to default
        '''
        self._icon = DEFAULT_ICON

    def remove_endpoint(self, endpoint: Endpoint, version: Optional[str] = None) -> None:
        '''
            Removes specified endpoint 
        '''
        self.get_version_info(version)._endpoints.remove(endpoint)

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
    
    def get_owner(self) -> User:
        '''
            Returns owner of service
        '''
        return self._owner
    
    def get_endpoints(self, version: Optional[str] = None) -> list[Endpoint]:
        '''
            Returns endpoints of service, returns latest version by default
        '''
        return self.get_version_info(version)._endpoints

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
    
    def get_docs(self, version: Optional[str] = None) -> List[str]:
        '''
            Returns docs
        '''

        return self.get_version_info(version)._docs
    
    def get_status(self) -> ServiceStatus:
        '''
            Returns status of service
        '''
        return self._status
    
    def get_status_reason(self) -> ServiceStatus:
        return self._status_reason

    def get_icon(self) -> str:
        '''
            Returns service's icon
        '''
        return self._icon

    def get_reviews(self) -> List[str]:
        '''
            Returns service's reviews
        '''
        return self._reviews
    
    def get_ratings(self) -> Dict[str, int]:
        '''
            Returns ratings of service
        '''
        return {
            'positive': self._upvotes,
            'negative': self._downvotes,
            'rating' : round(self._upvotes - self._downvotes, 2)
        }
    
    ################################
    #  Version Methods
    ################################

    def get_version_info(self, version: Optional[str]) -> ServiceVersionInfo:
        '''
            gets info related to specific version of service
            Returns latest version by default if no version is provided
            throws error if version not found
        '''
        if version is None:
            return self._version_info[0]
        
        versions = [ver for ver in self._version_info if ver._version_name == version]

        if len(versions) == 0:
            raise HTTPException(status_code=404, detail="Service version {version} not found in service")
        return versions[0]
        


    ################################
    #  Storage Methods
    ################################
    def to_json(self) -> dict[T, K]:
        '''
            Converts object into json,
        '''
        return {
            'id': self._id,
            'name' : self._name,
            'owner' : {
                'id' : self._owner.get_id(),
                'name' : self._owner.get_name(),
                'email' : self._owner.get_email()
            },
            'icon_url' : self._icon_url,
            'description' : self._description,
            'tags' : self._tags,
            'users' : self._users,
            'reviews': self._reviews,
            'upvotes': self._upvotes,
            'type': self._type,
            'icon': self._icon,
            'downvotes': self._downvotes,
            'status': self._status.name,
            'status_reason': self._status_reason,
            # fields denoting most current service version

            "versions": [version.to_json() for version in self._version_info]
        }
    
            

    def to_updated_json(self) -> dict[T, K]:
        '''
            Converts object into json, returning updated values for a pending
            update

            Notably only returns a single version - the version being updated
            and not the rest
        '''

        if self._status == ServiceStatus.UPDATE_PENDING:
            # version = self._pending_update.get_version()
            version = self.get_version_info(None)
            return {
                'id': self._id,
                'name' : self._pending_update.get_name(),
                'owner' : self._owner,
                'icon_url' : self._icon_url,
                'description' : self._pending_update.get_description(),
                'tags' : self._pending_update.get_tags(),
                'endpoints' : version._endpoints,
                # TODO: endpoints and docs update
                # 'endpoints': self._pending_update.get_endpoints(), 
                'docs' : version._docs,
                'users' : self._users,
                'reviews': self._reviews,
                'upvotes': self._upvotes,
                'type': self._type,
                'icon': self._icon,
                'downvotes': self._downvotes
            }
        else:
            return self.to_json()
    
    def to_summary_json(self) -> dict[T, K]:
        return {
            'id': self._id,
            'name': self._name,
            'owner': self._owner,
            'description': self._description,
            'icon_url': self._icon_url,
            'tags': self._tags
        }