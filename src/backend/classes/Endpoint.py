from Parameter import *
from Response import *
from typing import Optional

class Endpoint:

    '''
    Endpoint class which contains information and documentation for
    different endpoints of an API.

    Stores the following:
        link                Link of the endpoint
        title_description   Small description in line with the link
        main_description    Description of what the endpoint does
        tab:                Tab of endpoint (i.e. AUTH, SERVICE, etc.)
        parameters:         List of Parameters of the endpoint
        method:             Method of endpoint (i.e. GET, POST, etc.)

    '''
    # ALLOWED_TABS = {"AUTH", "SERVICE", "PAYMENT", "USER"}
    ALLOWED_METHODS = {"GET", "POST", "DELETE", "PUT"}

    def __init__(self,
                 link: str,
                 title_description: str,
                 main_description: str,
                 tab: str,
                 parameters: list[Parameter],
                 method: str,
                 responses: list[Response]) -> None:
        
    #    if tab not in self.ALLOWED_TABS:
    #        raise ValueError(f"Invalid tab: {tab}. Allowed tabs are: {self.ALLOWED_TABS}")
        
        if method not in self.ALLOWED_METHODS:
            raise ValueError(f"Invalid method: {method}. Allowed methods are: {self.ALLOWED_METHODS}")
        
        self._link = link
        self._title_description = title_description
        self._main_description = main_description
        self._tab = tab 
        self._parameters = parameters 
        self._method = method 
        self._responses = responses

    ################################
    #   Add Methods
    ################################

    def add_parameter(self, required: bool, type: str, name: str, value_type: str, example: Optional[str]) -> None:
        parameter_id = (len(self._parameters) + 1).to_string()
        self._parameters.append(
            Parameter(parameter_id, self._link, required, type, name, value_type, example)
        )
    
    def add_responses(self, code: str, desc: str, conditions: list[str], example: Optional[str]) -> None:
        self._responses.append(
            Response(code, desc, conditions, example)
        )
    
    ################################
    #   Remove Methods
    ################################

    def remove_parameter(self, parameter: Parameter) -> None:
        self._parameters.remove(parameter)
    
    def remove_responses(self, response: Response) -> None:
        self._responses.remove(response)

    ################################
    #   Get Methods
    ################################

    def get_link(self) -> str:
        '''
            Returns link of endpoint
        '''
        return self._link
    
    def get_title_description(self) -> str:
        '''
            Returns title description of endpoint
        '''
        return self._title_description
    
    def get_main_description(self) -> str:
        '''
            Returns main description of endpoint
        '''
        return self._main_description
    
    def get_tab(self) -> str:
        '''
            Returns tab of endpoint
        '''
        return self._tab
    
    def get_parameters(self) -> str:
        '''
            Returns parameters of endpoint
        '''
        return self._parameters
    
    def get_specified_parameter(self, id: str) -> Parameter:
        '''
            Returns a specified parameter, given an id
        '''
        for parameter in self._parameters:
            if parameter.get_id() == id:
                return parameter
        
        print("Error: Could not find specified parameter")
        return None
    
    def get_method(self) -> str:
        '''
            Returns method of endpoint
        '''
        return self._method 
    
    ################################
    #   Update Methods
    ################################

    def update_link(self, link: str) -> None:
        '''
            Updates link of endpoint
        '''
        self._link = link

    def update_title_description(self, desc: str) -> None:
        '''
            Updates title description of endpoint
        '''
        self._title_description = desc 

    def update_main_description(self, desc: str) -> None:
        '''
            Updates main descripton of endpoint
        '''
        self._main_description = desc 

    def update_tab(self, tab: str) -> None:
        '''
            Updates tab of endpoint
        '''
        self._tab = tab 

    def update_method(self, method: str) -> None:
        '''
            Updates method of endpoint
        '''
        self._method = method

#probably dont need this...

'''
    def update_parameter(self, id: str, endpoint_link: str, required: bool, type: str, name: str, value_type: str, example: Optional[str]) -> None:
        
            Updates parameter given the parameter id
        
        index = -1
        for parameter in self._parameters:
            if parameter.get_id() == id:
                index = self._parameters.index(parameter)
                break

        if index == -1:
            print("Error: Could not find specified parameter")
            return 
        
        self._parameters.remove(index)
        self._parameters.append(Parameter(id, endpoint_link, required, type, name, value_type, example))

'''
