from src.backend.classes.Comment import Comment
from typing import Union

class Review(Comment):

    '''
        Class which represents a review on APIOverflow. Inherits from Comment

        Requires:
            - id:              ID of review
            - reviewer:         Person creating the review (uid)
            - service:          Service review pertains to (sid)
            - rating:           'positive' or 'negative'
            - body:             Actual review content

        Also stores internally:
            - upvotes:          List of user IDs upvoting the review
            - downvotes:        List of user IDs downvoting the review
            - reply:            ReviewReply obj associated with this review
    '''

    def __init__(self,
                 rid: str,
                 reviewer: str,
                 service: str,
                 rating: str,
                 body: str
                ):
        
        # Set up parent class attributes
        super().__init__(rid, reviewer, service, body)

        # Given attributes
        self._rating = rating
        self._upvote = []
        self._downvote = []
        self._reply = None

    #############################
    #   Update methods
    #############################  
    def update_review(self, rating: str, body: str) -> None:
        '''
            Update the contents of the review
        '''
        self.update_content(body)
        self._rating = rating

    def update_vote(self, uid: str, _type: str) -> Union[bool, None]:
        '''
            Adds a vote to the review (expects either 'positive' or 'negative')
        '''
        # Check whether user has voted
        if uid in self._upvote or uid in self._downvote:
            return None

        # Add user's vote
        if _type == 'positive':
            self._upvote.append(uid)
        else:
            self._downvote.append(uid)

        return True

    def remove_vote(self, uid: str) -> bool:
        '''
            Removes user's vote on review
        '''

        if uid in self._upvote:
            self._upvote.remove(uid)
            return True
            
        elif uid in self._downvote:
            self._downvote.remove(uid)
            return True
        
        # If we reach here, user has not voted on this review
        return False

    def add_reply(self, rid: str) -> None:
        '''
            Adds reply to review
        '''
        self._reply = rid

    def remove_reply(self) -> None:
        '''
            Removes reply to review
        '''
        self._reply = None

    #############################
    #   Get methods
    #############################   
    def get_rating(self):
        '''
            Gets review's rating
        '''
        return self._rating
    
    def get_upvote(self):
        '''
            Gets review's upvotes 
        '''
        return len(self._upvote)
    
    def get_downvote(self):
        '''
            Gets review's downvotes
        '''
        return len(self._downvote)

    def get_net_vote(self):
        '''
            Gets the net vote value of review
        '''
        return len(self._upvote) - len(self._downvote)

    def get_reply(self):
        '''
            Returns reply if any
        '''
        return self._reply
    
    def get_upvote_ids(self):
        '''
            Gets review's upvotes ids
        '''
        return self._upvote
    
    def get_downvote_ids(self):
        '''
            Gets review's downvotes ids
        '''
        return self._downvote

    #############################
    #   JSON methods
    #############################
    def to_json(self, brief: bool = False, uid: str = ''):
        '''
            Returns a dict-format of the review info
                - brief = True makes a condensed version
                - uid option allows returning of indication of what user voted on review
        '''

        if brief:
            return {
                'rid': self._id,
                'reviewer': self.get_owner(),
                'service': self._service,
                'comment': self.get_content(),
                'type': self._rating,
                'timestamp': self.get_timestamp(),
                'e_timestamp': self.get_e_timestamp(),
                'upvotes': self.get_upvote(),
                'downvotes': self.get_downvote()
            }
        
        reply = None if self._reply is None else self._reply
        voted = ''
        if uid != '':
            if uid in self._upvote:
                voted = 'up'
            elif uid in self._downvote:
                voted = 'down'
        return {
                'rid': self._id,
                'reviewer': self._owner,
                'service': self._service,
                'comment': self._content,
                'type': self._rating,
                'upvotes': len(self._upvote),
                'downvotes': len(self._downvote),
                'timestamp': self.get_timestamp(),
                'edited': self.is_edited(),
                'e_timestamp': self.get_e_timestamp(),
                'reply' : reply,
                'voted' : voted
            }