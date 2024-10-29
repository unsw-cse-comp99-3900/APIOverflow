from typing import List
from src.backend.classes.Service import Service
from src.backend.classes.Endpoint import Endpoint


class API(Service):

    '''
        API class which represents an API uploaded to the platform.

        Inherits from Service
    
    '''

    def __init__(self,
                 sid: str,
                 name: str,
                 owner: str,
                 icon_url: str,
                 description: str,
                 tags: List[str],
                 endpoints: list[Endpoint]) -> None:
        super().__init__(sid, name, owner, icon_url, description, tags, endpoints, 'api')
    
    def get_type(self):
        '''
            Returns 'api'
        '''
        return self._type

    def update_api_details(self,
                 name: str,
                 description: str,
                 tags: List[str],
                 endpoints: list[Endpoint]):
        self._name = name
        self._description = description
        self._tags = tags
        self._endpoints = endpoints
