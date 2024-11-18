from typing import Optional, List
from pydantic import BaseModel, Field, model_validator


class Response(BaseModel):
   """
   Response class which contains information about the responses of HTTP
   requests and the conditions that need to be met.


   Attributes:
       code:        The code of the request (i.e., 200, 401, 400)
       description: Description of the code (i.e., OK, Failed, etc.)
       conditions:  List of conditions for the request (OR logic between conditions)
       example:     Example of success/failing values
   """
   code: str
   description: str
   conditions: List[str]
   example: Optional[str] = None


   @model_validator(mode='after')
   def set_default_example(self) -> 'Response':
       if self.example is None:  # Only set default if no example was provided
           self.example = f"No example given."
       return self




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



