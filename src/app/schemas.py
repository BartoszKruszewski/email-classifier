from pydantic import BaseModel, EmailStr, Field

from src.app.departments import Department


class MessageRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="The email address of the sender.",
        json_schema_extra={"example": "jan.kowalski@firma.pl"},
    )
    message: str = Field(
        ...,
        min_length=3,
        description="The unformatted text content of the message from the user.",
        json_schema_extra={"example": "Hello, I have a problem with my keyboard."},
    )


class RouteResponse(BaseModel):
    department: Department = Field(
        ...,
        description="The department to which the message was routed.",
    )
