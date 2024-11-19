from typing import *
from copy import deepcopy
from src.backend.classes.Document import Document
from src.backend.classes.User import User
from src.backend.classes.Tag import Tag, SYSTEM, CUSTOM

LIVE = 1

T = TypeVar("T")
defaults = [
    "API",
    "Microservice",
    "Productivity",
    "AI",
    "Public",
    "In Development",
    "Published",
    "Recently Updated"
]

DEFAULT_TAGS = [Tag(i, j, SYSTEM) for i, j in enumerate(defaults)]

DEFAULT_ICON_PATH = "static/imgs/default_icon.png"
DEFAULT_ICON = Document('0', DEFAULT_ICON_PATH, 'image/png')

schema = {
    'users' : [],
    'user_count' : 0,
    'max_user_count' : 0,
    'apis' : [],
    'api_count' : 0,
    'tags' : DEFAULT_TAGS.copy(),
    'tag_count' : len(DEFAULT_TAGS),
    'max_tag_count': len(DEFAULT_TAGS),
    'img_count' : 0,
    'docs_count': 1,
    'docs': [DEFAULT_ICON],
    'reviews' : [],
    'review_count': 0,
    'review_total': 0,
    'replys' : [],          # Yes I know it's 'replies' but it's for delete_items
    'reply_count': 0,
    'reply_total': 0
}

class Datastore:

    '''
    Datastore Class which acts as the backend's live storage and should be 
    created when server is launched.

    Globally stores everything

    '''

    def __init__(self) -> None:
        '''
            Constrcutor with default schema as initial store
        '''
        self.__store = deepcopy(schema)

    ######################################
    #   Loading and Saving Methods Methods
    ######################################
    def load_datastore(self) -> None:
        # TODO - load data from mongoDB
        pass

    def clear_datastore(self) -> None:
        self.__store = deepcopy(schema)

    ##################################
    #   Datastore Insertion Methods
    ##################################
    def add_user(self, user: T) -> None:
        '''
            Adds a user into the datastore
        '''
        self.__store['users'].append(user)
        self.__store['user_count'] += 1
        self.__store['max_user_count'] += 1
    
    def add_api(self, api: T) -> None:
        '''
            Adds an API into the datastore
        '''
        self.__store['apis'].append(api)
        self.__store['api_count'] += 1

    def add_tag(self, tag: T) -> Union[None, T]:
        '''
            Adds a tag into the datastore | returns None if dupe, otherwise Tag obj
        '''    

        # Shield against duplicates
        if tag in [tag.get_tag() for tag in self.__store['tags']]:
            return None

        # Create new tag
        new_tag = Tag(self.__store['max_tag_count'], tag, CUSTOM)
        self.__store['tags'].append(new_tag)
        self.__store['tag_count'] += 1
        self.__store['max_tag_count'] += 1
        return new_tag

    def add_img_count(self) -> None:
        '''
            Increments image counter
        '''
        self.__store['image_count'] += 1

    def add_docs(self, doc: T) -> None:
        '''
            Adds a document to the datastore
        '''
        self.__store['docs'].append(doc)
        self.__store['docs_count'] += 1

    def add_review(self, review: T) -> None:
        '''
            Adds a review to the datastore
        '''
        self.__store['reviews'].append(review)
        self.__store['review_count'] += 1
        self.__store['review_total'] += 1

    def add_reply(self, reply: T) -> None:
        '''
            Adds a reply to the datastore
        '''
        self.__store['replys'].append(reply)
        self.__store['reply_count'] += 1
        self.__store['reply_total'] += 1

    ################################
    #   Datastore Search Methods
    ################################
    def get_users(self) -> List[User]:
        '''
            Returns a list of all users
        '''
        return self.__store['users']
    
    def get_apis(self) -> List[T]:
        '''
            Returns a list of all apis
        '''
        return self.__store['apis']
    
    def get_tags(self) -> List[T]:
        '''
            Returns a list of all tags
        '''
        return self.__store['tags']

    def get_max_tags(self) -> int:
        '''
            Returns total number of tags created
        '''
        return self.__store['max_tag_count']

    def get_tag_by_name(self, tag: str) -> T | None:
        '''
            Returns a tag given a tag-name, else None
        '''
        for item in self.__store['tags']:
            if item.get_tag() == tag:
                return item
            
        return None

    def get_tag_ranking(self, num: int, custom: bool) -> list[dict[str, str | int]]:
        '''
            Returns a list of 'num' tags {tag: str, amt: int} in desc order
        '''
        # Sort list of tags 
        tags = []
        if custom:
            tags = [tag for tag in self.__store['tags'] if tag.get_type() == CUSTOM]
            tags.sort(key=lambda x : (-len(x.get_servers()), x.get_tag().lower()))
        else:
            tags = sorted(self.__store['tags'], key=lambda x : (-len(x.get_servers()), x.get_tag().lower()))
        
        # Screen for unapproved services
        output = []
        for tag in tags:
            for _service in tag.get_servers():
                service = self.get_api_by_id(_service)
                if service.get_status().value == LIVE:
                    output.append(tag)
        
        if len(output) < num:
            return {
                'tags': [tag.to_json() for tag in output]
            }

        return {
            'tags': [tag.to_json() for tag in output[:num]]
        }

    def get_docs(self) -> List[T]:
        '''
            Returns a list of all users
        '''
        return self.__store['docs']

    def get_api_by_id(self, eid: str) -> T | None:
        '''
            Returns with the given ID, or None if cannot find user
        '''
        for item in self.__store['apis']:
            if item.get_id() == eid:
                return item
        
        return None

    def get_user_by_id(self, eid: str) -> T | None:
        '''
            Returns with user obj base on given ID, or None if cannot find user
        '''
        for item in self.__store['users']:
            if item.get_id() == eid:
                return item

        return None

    def get_user_by_name(self, name: str) -> T | None:
        '''
            Returns with user obj based on username, or None if cannot find user
        '''
        for item in self.__store['users']:
            if item.get_name() == name:
                return item
            
        return None
    
    def get_user_by_email(self, email: str) -> T | None:
        '''
            Returns with user obj based on email, or None if cannot find user
        '''
        for item in self.__store['users']:
            if item.get_email() == email:
                return item
            
        return None

    def get_doc_by_id(self, eid: str) -> T | None:
        '''
            Returns with user obj base on given ID, or None if cannot find user
        '''
        for item in self.__store['docs']:
            print(item.get_id(), type(item.get_id()), eid, type(eid), item.get_id() == eid)
            if item.get_id() == eid:
                return item

        return None

    def get_review_by_id(self, rid: str) -> T | None:
        '''
            Retrieves a review by id if it exists, else None
        '''
        for item in self.__store['reviews']:
            # print(f"RID: {rid} | Item ID: {item.get_id()} Comparison: {rid == item.get_id()}")
            if item.get_id() == rid:
                return item

        return None

    def get_reviews(self) -> List[T]:
        '''
            Gets all reviews
        '''
        return self.__store['reviews']

    def get_user_apis(self, eid: str) -> List[T]:
        '''
            Returns a list of APIs owned by the user with the given user ID.
        '''
        user_apis = []
        for item in self.__store['apis']:
            owner = item.get_owner()
            if str(eid) in owner.get_id():
                api_info = {
                    'id': item.get_id(),
                    'name': item.get_name(),
                    'owner': owner.get_displayname(),
                    'description': item.get_description(),
                    'icon_url': item.get_icon_url(),
                    'tags': item.get_tags(),
                    'pay_model': item.get_pay_model()
                }
                user_apis.append(api_info)
        return user_apis

    def num_users(self) -> int:
        '''
            Returns number of users
        '''
        return self.__store['user_count']
    
    def max_num_users(self) -> int:
        '''
            Returns max number of users
        '''
        return self.__store['max_user_count']

    def num_apis(self) -> int:
        '''
            Returns number of APIs
        '''
        return self.__store['api_count']

    def num_tags(self) -> int:
        '''
            Returns number of tags
        '''
        return self.__store['tag_count']

    def num_imgs(self) -> int:
        '''
            Returns number of imgs stored
        '''
        return self.__store['img_count']

    def num_docs(self) -> int:
        '''
            Returns number of docs
        '''
        return self.__store['docs_count']

    def num_reviews(self) -> int:
        '''
            Returns number of reviews
        '''
        return self.__store['review_count']
    
    def total_reviews(self) -> int:
        '''
            Returns number of reviews created in total
        '''
        return self.__store['review_total']

    def get_reply_by_id(self, rid: str) -> T | None:
        '''
            Retrieves a reply by id if it exists, else None
        '''
        for item in self.__store['replys']:
            if item.get_id() == rid:
                return item

        return None

    def get_replies(self) -> List[T]:
        '''
            Returns all replies made
        '''
        return self.__store['replys']
    
    def total_replies(self) -> int:
        '''
            Returns totla number of all replies
        '''
        return self.__store['reply_total']

    ################################
    #   Datastore Deletion Methods
    ################################
    def delete_item(self, eid: int, i_type: Literal['user', 'api', 'review', 'reply']) -> None:
        '''
            Deletes an item from the database (not tags)
        '''
        search_term = i_type + "s"
        term_count = i_type + "_count"
        for item in self.__store[search_term]:
            if item.get_id() == eid:
                self.__store[search_term].remove(item)
                self.__store[term_count] -= 1
                return

    def delete_tag(self, tag: str) -> Union[None, bool]:
        ''''
            Deletes a tag from the database & corresponding servers
        '''
        for _tag in self.__store['tags']:
            if _tag.get_tag() == tag:

                # Disassociate tag from each server
                for server in _tag.get_servers():
                    server.remove_tag(tag)

                # Remove tag from store
                self.__store['tags'].remove(_tag)
                self.__store['tag_count'] -= 1
                return True
            
        return None

print('Loading Datastore...')

global data_store
data_store = Datastore()
#data_store.load_database()
