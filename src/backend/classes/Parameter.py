from typing import Optional

class Parameter:
    '''
    Parameter class which abstracts and contains information about
    parameters for endpoints.

    Stores the following:
        id:             ID of parameter
        endpoint_link:  Link of the endpoint that this parameter is attached to
        required:       Whether the parameter is required or not
        type:           Type of parameter (i.e. head, body, etc.)
        name:           Name of the parameter
        value_type:     Type of the given values (i.e. string, int, etc.)
                        However, since this is for DISPLAY ONLY, we can just
                        implement this as a string.
        example:        Example of possible values.
        

    '''

    # not sure if we need this...?
    ALLOWED_TYPES = {"HEADER", "BODY", "QUERY", "PATH"}

    def __init__(self,
                id: str,
                endpoint_link: str,
                required: bool,
                type: str,
                name: str,
                value_type: str,
                example: Optional[str]) -> None:

        if type not in self.ALLOWED_TYPES:
            raise ValueError(f"Invalid type: {type}. Allowed types are: {self.ALLOWED_TYPES}")
        
        self._id = id
        self._endpoint_link = endpoint_link
        self._required = required 
        self._type = type
        self._name = name
        self._value_type = value_type
        if example is not None:
            self._example = example
        else:
            self._example = f"Any {value_type}"

    ################################
    #   Get Methods
    ################################

    def get_endpoint(self) -> str:
        '''
            Returns the endpoint that this parameter is attached to
        '''
        return self._endpoint_link
    
    def get_id(self) -> str:
        '''
            Returns the parameter id
        '''
        return self._id
    
    def get_required(self) -> str:
        '''
            Returns whether or not the parameter is required
        '''
        return self._required
    
    def get_type(self) -> str:
        '''
            Returns the type of parameter
        '''
        return self._type 
    
    def get_name(self) -> str:
        '''
            Returns the parameter name
        '''
        return self._name 
    
    def get_value_type(self) -> str:
        '''
            Returns the value type of parameter
        '''
        return self._value_type
    
    def get_example(self) -> str:
        '''
            Returns the example
        '''
        return self._example
    
    ################################
    #   Update Methods
    ################################

    def update_required(self, required: bool) -> None:
        '''
            Updates the endpoint link
        '''
        self._required = required
    
    def update_type(self, type: str) -> None:
        '''
            Updates the endpoint link
        '''
        self._type = type 

    def update_name(self, name: str) -> None:
        '''
            Updates the endpoint link
        '''
        self._name = name 

    def update_value_type(self, value_type: str) -> None:
        '''
            Updates the endpoint link
        '''
        self._value_type = value_type 

    def update_example(self, example: str) -> None:
        '''
            Updates the endpoint link
        '''
        self._example = example