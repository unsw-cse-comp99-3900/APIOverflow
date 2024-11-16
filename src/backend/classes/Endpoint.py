from typing import List, Optional, ClassVar
from pydantic import BaseModel, Field, field_validator
from src.backend.classes.Parameter import Parameter
from src.backend.classes.Response import Response

class Endpoint(BaseModel):
    link: str
    title_description: str
    main_description: str
    tab: str
    parameters: List[Parameter]
    method: str
    responses: List[Response]

    ALLOWED_METHODS: ClassVar[set] = {'DELETE', 'PUT', 'POST', 'GET'}

    @field_validator("method")
    def validate_method(cls, value):
        if value not in cls.ALLOWED_METHODS:
            raise ValueError(f"Invalid method: {value}. Allowed methods are: {cls.ALLOWED_METHODS}")
        return value

    # Add methods
    def add_parameter(self, required: bool, type: str, name: str, value_type: str, example: Optional[str]) -> None:
        parameter_id = str(len(self.parameters) + 1)
        self.parameters.append(Parameter(parameter_id, self.link, required, type, name, value_type, example))

    def add_response(self, code: str, desc: str, conditions: List[str], example: Optional[str]) -> None:
        self.responses.append(Response(code, desc, conditions, example))

    # Remove methods
    def remove_parameter(self, parameter: Parameter) -> None:
        self.parameters.remove(parameter)

    def remove_response(self, response: Response) -> None:
        self.responses.remove(response)

    # Update methods (direct assignment works, but update methods can provide validation if needed)
    def update_link(self, link: str) -> None:
        self.link = link

    def update_title_description(self, desc: str) -> None:
        self.title_description = desc

    def update_main_description(self, desc: str) -> None:
        self.main_description = desc

    def update_tab(self, tab: str) -> None:
        self.tab = tab

    def update_method(self, method: str) -> None:
        self.method = method