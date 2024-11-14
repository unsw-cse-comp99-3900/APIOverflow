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
PENDING_OPTIONS = ["PENDING", "UPDATE_PENDING"]
LIVE_OPTIONS = ["LIVE", "UPDATE_PENDING", "UPDATE_REJECTED"]

T = TypeVar("T")
K = TypeVar("K")
DEFAULT_ICON = '0'

# API Changes
# Changes by wj:
# - "endpoint" field to "endpoints"
# - endpoints field is now a [Endpoint] instead of a str (consult with wj for details)


# /service/add: added "version_name" and "version_description" fields
#  - currently these give a default value to not break existing things
#  - but pls change so users must provide these strings
#  - throws error if version_name is ""

# /service/upload_docs : Added "version_name" field
# similarly currently by default uploads doc to most recently created service version
# to not break existing things
# pls provide version_name field

#
# /service/get: 
#  - REMOVED FIELDS endpoints and docs
#  - Added Field "newly_created"
#  - Added field: versions: [{
            # "version_name": name of version(str)
            # "endpoints": list of endpoints (whatever it was before),
            # "version_description": Additional description for version(str),
            # "docs": documents (whatever it was before)
            # "status": name of status: 
            # "status_reason": reason for status
            # "newly_created": bool for if newly created
# }]
# Notably returns everything even if they aren't LIVE so that you can say display it on someone's profile
# newly_created refers to if service and/or service_version was just created and
# has not yet been approved
# - It is important that FE does NOT display a status version if newly_created == True
# when displaying service details
# Status is one of ["LIVE", "PENDING", "REJECTED", "UPDATE_PENDING", "UPDATE_REJECTED"]
# 
# /service/update: No longer contains endpoints field (only updates global fields)
# changed from put to POST request


# /admin/service/approve: POST
# - changed to take these fields:
# {
#     "sid" : str,
#     "approved" : bool,
#     "reason" : str,
#     "service_global": bool, # if we are updating service_global fields
#     "version" : Optional[str], # if we are updating version, provide name
# }
# IF updating new service: service_global == True && provide version
# IF updating only service_global: service_global == True and don't provide version field
# IF updating only version: service_global == False and provide version

# /admin/get/services
# - changed to take no fields:
# - now returns:
#         {
#             "new_services": [{
#                                All global fields,
#                                "version_fields": {All version Fields}
#                             }]
#             "global_updates": [{All global fields}]
#             "version_updates":[{All version Fields}]
#         }
# Global fields:
# - "id"
# - "name"
# - "description"
# - "tags"

# Version Fields:
# - "id":                 id of service
# - "name":               name of service
# - "version_name":       
# - "endpoints":
# - "version_description":


# New REST Endpoints:
# /service/version/add : POST
# Fields:
#  - sid: str                        # id of service 
#  - version_name: str               # name of new version
#  - endpoints: List[Endpoint]       # endpoints of new version
#  - version_description: str        # Additional details pertaining new version   
# - throws error if invalid sid, version_name same as existing version_name or
#   version_name == "" or if you try to create a new version before a newly
#  created service has been approved yet

# /service/version/update: POST
# fields:
# - sid: str                        # id of service 
# - version_name: str               # name of new version
# - new_version_name: Optional[str] = None # Optional field if we are renaming the version_name
# - endpoints: List[Endpoint]       # endpoints of new version
# - version_description: str        # Additional details pertaining new version   


# /service/version/delete : DELETE
# Fields: sid and version_name
# throws error if invlaid sid, invalid version_name or service contains only one version



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
        self._newly_created: bool = True

    def update_newly_created(self):
        self._newly_created = False

    def to_json(self):
        return {
            "version_name": self._version_name,
            "endpoints": self._endpoints,
            "version_description": self._version_description,
            "docs": self._docs,
            "status": self._status.name,
            "status_reason": self._status_reason,
            "newly_created": self._newly_created

        }
    
    def to_updated_json(self, id: str, name: str):
        if self._status == ServiceStatus.PENDING:
            updated_fields = self
        elif self._status == ServiceStatus.UPDATE_PENDING:
            updated_fields = self._pending_update

        if self._status.name in PENDING_OPTIONS:
            return {
                "id": id,
                "name": name,
                "version_name": updated_fields.get_version_name(),
                "endpoints": updated_fields.get_endpoints(),
                "version_description": updated_fields.get_version_description()
            }
        return None
    
    def update_status(self, status: ServiceStatus, reason: str):
        self._status = status
        self._status_reason = reason
    
    def get_status(self):
        return self._status
    
    def get_version_name(self):
        return self._version_name
    
    def get_endpoints(self):
        return self._endpoints
    
    def get_version_description(self):
        return self._version_description
    
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
        self._newly_created: bool = True
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

    def add_docs(self, docs: List[int], version) -> None:
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
    
    def update_newly_created(self):
        self._newly_created = False

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

    def get_newly_created(self) -> bool:
        return self._newly_created
    
    ################################
    #  Version Methods
    ################################

    def add_service_version(self, version_name: str, endpoints: List[Endpoint], version_description: str):
        if version_name == "":
            raise HTTPException(status_code=400, detail='Version name cannot be empty')

        if self.contains_version(version_name):
            raise HTTPException(status_code=404, detail='Version names must be Unique')
        
        if len(self._version_info) > 0 and self._newly_created:
            raise HTTPException(status_code=404, detail='Original Service must be approved before creating new version')
        
        # maintain version_info has most recently added version at front of list
        self._version_info.insert(0,
            ServiceVersionInfo(version_name, endpoints, version_description)
        )
    
    def contains_version(self, version_name) -> bool:
        return any(version._version_name == version_name for version in self._version_info)

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

    def get_all_versions(self) -> List[ServiceVersionInfo]:
        return self._version_info
    
    def get_latest_version(self) -> ServiceVersionInfo:
        return self._version_info[0]
    
    def update_service_version(self, version_name: str, new_version_name: Optional[str], endpoints: List[Endpoint], version_description: str):
        version : ServiceVersionInfo = self.get_version_info(version_name)

        if new_version_name is not None:
            if new_version_name == "":
                raise HTTPException(status_code=400, detail='new version name cannot be empty')

            if new_version_name != version_name and self.contains_version(new_version_name):
                raise HTTPException(status_code=404, detail='Version names must be Unique')

            version_name = new_version_name
        
        version.create_pending_update(version_name, endpoints, version_description)
    
    def remove_version(self, version_name: str) -> None:
        if len(self._version_info) == 1:
            raise HTTPException(status_code=404, detail="Cannot Delete last version of service")

        versions = [ver for ver in self._version_info if ver._version_name != version_name]

        if len(versions) == len(self._version_info):
            raise HTTPException(status_code=404, detail="Service version {version_name} not found in service")
        
        assert len(versions) + 1 == len(self._version_info)
        self._version_info = versions


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
            'newly_created': self._newly_created,
            # fields denoting most current service version

            "versions": [version.to_json() for version in self._version_info]
        }
    
            

    def to_updated_json(self) -> dict[T, K]:
        '''
            Converts object into json, returning updated values for a pending
            update for all global fields, status should already be in PENDING
            OPTIONS
        '''
        if self._status == ServiceStatus.UPDATE_PENDING:
            updated_fields = self._pending_update
        elif self._status == ServiceStatus.PENDING:
            updated_fields = self

        if self._status.name in PENDING_OPTIONS:
            return {
                "id": self._id,
                "name": updated_fields.get_name(),
                "description": updated_fields.get_description(),
                "tags": updated_fields.get_tags()
            }
 
        return None
    
    def to_summary_json(self) -> dict[T, K]:
        return {
            'id': self._id,
            'name': self._name,
            'owner': self._owner,
            'description': self._description,
            'icon_url': self._icon_url,
            'tags': self._tags
        }