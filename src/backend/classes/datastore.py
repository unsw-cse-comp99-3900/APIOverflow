from typing import *
from src.backend.classes.Document import Document

T = TypeVar("T")
DEFAULT_TAGS = [
    "API",
    "Microservice",
    "Productivity",
    "AI",
    "Public",
    "In Development",
    "Published",
    "Recently Updated"
]

DEFAULT_ICON_PATH = "/static/imgs/default_icon0.png"
DEFAULT_ICON = Document('0', DEFAULT_ICON_PATH, 'image/png')

schema = {
    'users' : [],
    'user_count' : 0,
    'apis' : [],
    'api_count' : 0,
    'tags' : DEFAULT_TAGS.copy(),
    'tag_count' : len(DEFAULT_TAGS),
    'img_count' : 0,
    'docs_count': 1,
    'docs': [DEFAULT_ICON],
    'reviews' : [],
    'review_count': 0,
    'review_total': 0
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
        self.__store = schema

    ######################################
    #   Loading and Saving Methods Methods
    ######################################
    def load_datastore(self) -> None:
        # TODO - load data from mongoDB
        pass

    def clear_datastore(self) -> None:
        self.__store = {
                            'users' : [],
                            'user_count' : 0,
                            'apis' : [],
                            'api_count' : 0,
                            'tags' : DEFAULT_TAGS.copy(),
                            'tag_count' : len(DEFAULT_TAGS),
                            'img_count' : 0,
                            'docs_count': 1,
                            'docs': [DEFAULT_ICON],
                            'reviews' : [],
                            'review_count': 0,
                            'review_total': 0
                        }

    ##################################
    #   Datastore Insertion Methods
    ##################################
    def add_user(self, user: T) -> None:
        '''
            Adds a user into the datastore
        '''
        self.__store['users'].append(user)
        self.__store['user_count'] += 1
    
    def add_api(self, api: T) -> None:
        '''
            Adds an API into the datastore
        '''
        self.__store['apis'].append(api)
        self.__store['api_count'] += 1

    def add_tag(self, tag: str) -> Union[None, bool]:
        '''
            Adds a tag into the datastore
        '''    

        # Shield against duplicates
        if tag in self.__store['tags']:
            print(self.__store['tags'])
            return None

        self.__store['tags'].append(tag)
        self.__store['tag_count'] += 1
        return True

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

    ################################
    #   Datastore Search Methods
    ################################
    def get_users(self) -> List[T]:
        '''
            Returns a list of all users
        '''
        return self.__store['users']
    
    def get_apis(self) -> List[T]:
        '''
            Returns a list of all apis
        '''
        return self.__store['apis']
    
    def get_tags(self) -> List[str]:
        '''
            Returns a list of all tags
        '''
        return self.__store['tags']

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
            print("Item's name: %s | Name wanted: %s", item.get_name(), name)
            if item.get_name() == name:
                return item
            
        return None

    def get_doc_by_id(self, eid: str) -> T | None:
        '''
            Returns with user obj base on given ID, or None if cannot find user
        '''
        for item in self.__store['docs']:
            # print(item.get_id(), type(item.get_id()), eid, type(eid), item.get_id() == eid)
            if item.get_id() == eid:
                return item

        return None

    def get_review_by_id(self, rid: str) -> T | None:
        '''
            Retrieves a review by id if it exists, else None
        '''
        for item in self.__store['reviews']:
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
            owners = item.get_owner()
            if str(eid) in owners:
                api_info = {
                    'id': item.get_id(),
                    'name': item.get_name(),
                    'owner': item.get_owner(),
                    'description': item.get_description(),
                    'icon_url': item.get_icon_url(),
                    'tags': item.get_tags()
                }
                user_apis.append(api_info)
        return user_apis

    def num_users(self) -> int:
        '''
            Returns number of users
        '''
        return self.__store['user_count']

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

    ################################
    #   Datastore Deletion Methods
    ################################
    def delete_item(self, eid: int, i_type: Literal['user', 'api', 'review']) -> None:
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
            Deletes a tag from the database
        '''
        for _tag in self.__store['tags']:
            if _tag == tag:
                self.__store['tags'].remove(tag)
                self.__store['tag_count'] -= 1
                return True
        return None

print('Loading Datastore...')

global data_store
data_store = Datastore()
#data_store.load_database()
