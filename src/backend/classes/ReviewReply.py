from src.backend.classes.Comment import Comment

class ReviewReply(Comment):

    '''
        Class which represents a review reply on APIOverflow. Inherits from Comment

        Requires:
            - id:               ID of review
            - reviewer:         Person creating the review (uid)
            - service:          Service review pertains to (sid)
            - body:             Actual review content
            - parent:           Parent review this obj is replying to (rid)

    '''
    
    def __init__(self, id: str, reviewer: str, service: str, body: str, parent: str) -> None:
        
        # Set up parent class attributes
        super().__init__(id, reviewer, service, body)

        self._parent = parent
    
    #############################
    #   Get methods
    #############################
    def get_review(self) -> str:
        '''
            Returns id of parent review
        '''
        return self._parent
    

    #############################
    #   JSON methods
    #############################
    def to_json(self, brief: bool = False):
        '''
            Returns a dict-format of the review info
                - brief = True makes a condensed version
                - uid option allows returning of indication of what user voted on review
        '''

        if brief:
            return {
                'rid': self.get_id(),
                'service': self.get_service(),
                'timestamp': self.get_timestamp(),
                'e_timestamp': self.get_e_timestamp()
            }

        return {
                'rid': self._id,
                'reviewer': self._owner,
                'service': self._service,
                'comment': self._content,
                'timestamp': self.get_timestamp(),
                'edited': self.is_edited(),
                'e_timestamp': self.get_content(),
            }