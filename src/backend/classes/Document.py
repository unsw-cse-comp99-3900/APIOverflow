class Document:

    '''
        Document class representing a document uploaded to the platform
    '''

    def __init__(self, id: str, path: str, type: str) -> None:
        self._id = id
        self._path = path
        self._type = type
    
    ################################
    #   Get Methods
    ################################
    def get_id(self) -> str:
        '''
            Method which gets id of document
        '''
        return self._id

    def get_path(self) -> str:
        '''
            Method which gets path of document
        '''
        return self._path
    
    def get_type(self) -> str:
        '''
            Method which gets document type
        '''
        return self._type