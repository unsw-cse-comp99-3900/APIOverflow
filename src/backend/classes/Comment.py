from datetime import datetime

class Comment:

    '''
        An Abstract Class which represents a comment on APIOverflow

        Requires:
            - cid:              ID of comment
            - owner:            Person creating the comment (uid)
            - parent:           Parent body the comment pertains to (id)
            - body:             Actual comment content

        Additional attributes:
            - timestamp:        Datetime of when comment was created

    '''

    def __init__(self,
                 cid: str,
                 owner: str,
                 parent: str,
                 body: str
                ):
        
        # Given attributes
        self._id = cid
        self._owner = owner
        self._parent = parent
        self._body = body

        self._timestamp = datetime.now()

    #############################
    #   Update methods
    #############################  
    def update_comment(self, body: str) -> None:
        '''
            Update the contents of the comment
        '''
        self._body = body

    #############################
    #   Get methods
    #############################
    def get_id(self):
        '''
            Returns id of review
        '''
        return self._id
    
    def get_owner(self):
        '''
            Gets user who wrote the comment
        '''
        return self._owner

    def get_parent(self):
        '''
            Returns id of service review is related to
        '''
        return self._parent
      
    def get_body(self):
        '''
            Returns review text
        '''
        return self._body
    
    def get_timestamp(self):
        '''
            Returns time comment was created
        '''
        return self._timestamp.strftime('%d %b %Y at %I:%M%p')

    #############################
    #   JSON methods
    #############################
    def to_json(self, brief: bool = False):
        '''
            Returns a dict-format of the review info
                - brief = True makes a condensed version
        '''

        if brief:
            return {
                'rid': self._id
            }
        
        return {
                'rid': self._id,
                'comment': self._body
            }
