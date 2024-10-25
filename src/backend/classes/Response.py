from typing import Optional

class Response:
    '''
    Response class which contains information about the responses of HTTP
    requests and the conditions of which are met

    Stores the following:
        code:           The code of the request (i.e. 200, 401, 400)
        description:    Description of the code (i.e. OK, Failed, etc.)
        conditions:     List of conditions of the request (i.e. If any of the following are true:...) 
                        Works as OR operator.  
        example:        Example of success/failing values     

    '''

    def __init__(self,
                code: str,
                description: str,
                conditions: list[str],
                example: Optional[str]) -> None:
        
        self._code = code
        self._description = description
        self._conditions = conditions
        if example is not None:
            self._example = example
        else:
            self._example = "No example given."

    ################################
    #   Get Methods
    ################################

    def get_code(self) -> str:
        '''
            Returns code
        '''
        return self._code 
    
    def get_description(self) -> str:
        '''
            Returns description
        '''
        return self._description 

    def get_conditions(self) -> list[str]:
        '''
            Returns conditions
        '''
        return self._code  
    
    def get_example(self) -> Optional[str]:
        '''
            Returns conditions
        '''
        return self._example 
    
    ################################
    #   Update Methods
    ################################

    def update_code(self, code: str) -> None:
        '''
            Updates code
        '''
        self._code = code

    def update_description(self, desc: str) -> None:
        '''
            Updates desc
        '''
        self._description: desc 

    def update_conditions(self, conditions: list[str]) -> None:
        '''
            Updates conditions
        '''
        self._conditions = conditions 

    def update_example(self, example: Optional[str]) -> None:
        '''
            Updates example
        '''
        self._example = example