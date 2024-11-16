from typing import Literal

SYSTEM = 0
CUSTOM = 1

class Tag:

    '''
        Class which represents a Tag in APIOverflow

        Requires:
            - tid:      Id of tag
            - tag:      String of tag itself
            - type:     Type of tag [SYSTEM | CUSTOM]
            
        Also stores:
            - servers:  Ids of servers tag belongs to

    '''

    def __init__(self, tid: str, tag: str, type: int):
        self._id = tid
        self._tag = tag
        self._type = type

        # Custom vars
        self._servers  = []

    ################################
    #   Add Methods
    ################################
    def add_server(self, sid: str) -> None:
        '''
            Adds a server to its collection - ignores duplicate additions
        '''
        if sid in self._servers:
            return
        self._servers.append(sid)
    
    ################################
    #   Get Methods
    ################################
    def get_id(self) -> str:
        '''
            Returns id of tag
        '''
        return self._id
    
    def get_tag(self) -> str:
        '''
            Gets content of tag
        '''
        return self._tag
    
    def get_type(self) -> int:
        '''
            Gets tag type
        '''
        return self._type
    
    def get_servers(self) -> list[str]:
        '''
            Returns list of servers using this tag
        '''
        return self._servers

    ################################
    #   Remove Methods
    ################################
    def remove_server(self, sid: str) -> None:
        '''
            Removes a server from tag collection
        '''
        if sid not in self._servers:
            return
        self._servers.remove(sid)

    def to_json(self) -> None:
        '''
            Converts tag to readable format
        '''
        return {
            'tid': self._id,
            'tag': self._tag,
            'type': self._type,
            'num': len(self._servers)
        }
