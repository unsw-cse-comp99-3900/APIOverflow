from typing import List
from src.backend.classes.Service import Service
from src.backend.classes.Endpoint import Endpoint
from src.backend.classes.User import User

class API(Service):

    '''
        API class which represents an API uploaded to the platform.

        Inherits from Service
    
    '''

    def __init__(self,
                 sid: str,
                 name: str,
                 owner: User,
                 icon_url: str,
                 description: str,
                 tags: List[str],
                 endpoints: List[Endpoint],
                 version_name: str,
                 version_description: str
                 ) -> None:
        super().__init__(
            sid, name, owner, icon_url, description, tags, endpoints, 'api',
            version_name, version_description)
    
    def get_type(self):
        '''
            Returns 'api'
        '''
        return self._type
