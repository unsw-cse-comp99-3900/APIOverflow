from typing import TypeVar
from APIOverflow.src.backend.classes.datastore import data_store
from APIOverflow.src.backend.server.auth import manager

T = TypeVar('T')
K = TypeVar('K')

def add_service_wrapper(packet: dict[T, K]) -> dict[T, K]:
    '''
        Wrapper which extracts information from packet and verifies
        user information

        Raises:     HTTP Error 401
        Returns:    {
                        sid
                        name
                        owner
                        description
                        icon_url
                        tags
                    }
    '''
