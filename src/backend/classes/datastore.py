from typing import *

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

schema = {
    'users' : [],
    'user_count' : 0,
    'apis' : [],
    'api_count' : 0,
    'tags' : DEFAULT_TAGS,
    'tag_count' : 0,
    'img_count' : 0
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
                            'tags' : DEFAULT_TAGS,
                            'tag_count' : 0,
                            'img_count' : 0
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

    def add_tag(self, tag: str) -> None:
        '''
            Adds a tag into the datastore
        '''    
        self.__store['tags'].append(tag)
        self.__store['tag_count'] += 1

    def add_img_count(self) -> None:
        '''
            Increments image counter
        '''
        self.__store['image_count'] += 1

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
            Returns with the given ID, or None if cannot find user
        '''
        for item in self.__store['users']:
            if item.get_id() == eid:
                return item
        
        return None

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
    
    ################################
    #   Datastore Deletion Methods
    ################################
    def delete_item(self, eid: int, i_type: Literal['user', 'api']) -> None:
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

    def delete_tag(self, tag: str) -> None:
        ''''
            Deletes a tag from the database
        '''
        for _tag in self.__store['tags']:
            if _tag == tag:
                self.__store['tags'].remove(tag)
                self.__store['tag_count'] -= 1
                return

print('Loading Datastore...')

global data_store
data_store = Datastore()
#data_store.load_database()
