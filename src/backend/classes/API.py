from typing import List
from src.backend.classes.Service import Service

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
                 tags: List[str]) -> None:
        super().__init__(sid, name, owner, icon_url, description, tags, 'api')
    
    def get_type(self):
        '''
            Returns 'api'
        '''
        return self._type