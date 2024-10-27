LIVE = '1'
PENDING = '0'
REJECTED = '-1'

class Review:

    '''
        Class which represents a review on APIOverflow

        Requires:
            - rid:              ID of review
            - reviewer:         Person creating the review (uid)
            - service:          Service review pertains to (sid)
            - title:            Title of review
            - rating:           'positive' or 'negative'
            - body:             Actual review content

        Also stores internally:
            - status:           Status of the review (live, pending, rejected)
    '''

    def __init__(self,
                 rid: str, 
                 reviewer: str, 
                 service: str,
                 title: str,
                 rating: str,
                 body: str
                ):
        
        # Given attributes
        self._id = rid
        self._reviewer = reviewer
        self._service = service
        self._title = title
        self._rating = rating
        self._body = body

        # Other atributes
        self._status = PENDING
        self._status_reason = ''

    #############################
    #   Update methods
    #############################
    def update_status(self, status: str, reason: str = ''):
        '''
            Update status of review
        '''
        self._status = status
        self._status_reason = reason
    
    def update_review(self, title: str, rating: str, body: str) -> None:
        '''
            Update the contents of the review
        '''
        self.update_status(PENDING, '')
        self._title = title
        self._rating = rating
        self._body = body

    #############################
    #   Get methods
    #############################
    def get_id(self):
        '''
            Returns id of review
        '''
        return self._id
    
    def get_reviewer(self):
        '''
            Gets user who wrote reviewer
        '''
        return self._reviewer

    def get_service(self):
        '''
            Returns id of service review is related to
        '''
        return self._service
    
    def get_title(self):
        '''
            Gets title of review
        '''
        return self._title
    
    def get_body(self):
        '''
            Returns review text
        '''
        return self._body
    
    def get_rating(self):
        '''
            Gets review's rating
        '''
        return self._rating

    def get_status(self):
        '''
            Returns review's status
        '''
        return self._status
    
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
                'rid': self._id,
                'service': self._service,
                'title': self._title,
                'type': self._rating,
                'status': self._status
            }
        
        return {
                'rid': self._id,
                'reviewer': self._reviewer,
                'service': self._service,
                'title': self._title,
                'comment': self._body,
                'type': self._rating,
                'status': self._status
            }