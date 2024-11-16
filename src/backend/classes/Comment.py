from datetime import datetime

class Comment:

    '''
        Class which represents a 'comment' on APIOverflow.

        Requires:
            - id:               ID of comment
            - reviewer:         Person creating the comment (uid)
            - service:          Service comment pertains to (sid)
            - body:             Actual comment content

        Internally store:
            - timestamp:        Timestamp of when comment was created
            - edited:           Bool indicating whether comment has been edited
            - e_timestamp:      Timestamp of last edit made, if any

    '''

    def __init__(self, id: str, reviewer: str, service: str, body: str) -> None:
        self._id = id
        self._owner = reviewer
        self._service = service
        self._content = body

        # Internal timestamp
        self._timestamp = datetime.now()
        self._edited = False
        self._e_timestamp = None

    #############################
    #   Update methods
    #############################  
    def update_content(self, body: str) -> None:
        '''
            Method to edit body of comment
        '''
        self._content = body
        self._edited = True
        self._e_timestamp = datetime.now()

    #############################
    #   Get methods
    #############################  
    def get_id(self) -> str:
        '''
            Returns id
        '''
        return self._id
    
    def get_owner(self) -> str:
        '''
            Returns id of comment owner
        '''
        return self._owner

    def get_content(self) -> str:
        '''
            Returns comment's content
        '''
        return self._content
    
    def get_service(self) -> str:
        '''
            Returns service comment belongs to
        '''
        return self._service

    def get_timestamp(self) -> str:
        '''
            Returns timestamp of comment when created
        '''
        return self._timestamp.strftime("%-I:%M%p on %-d %b %Y")
    
    def is_edited(self) -> bool:
        '''
            Returns whether comment has been edited
        '''
        return self._edited

    def get_e_timestamp(self) -> str:
        '''
            Returns timestamp of when comment was last edited
        '''
        if self._e_timestamp is None:
            return None
        return self._e_timestamp.strftime("%-I:%M%p on %-d %b %Y")
