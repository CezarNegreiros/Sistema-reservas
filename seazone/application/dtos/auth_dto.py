from pydantic import BaseModel


class CreateUserDTO(BaseModel):
    email: str
    password: str


class LoginDTO(BaseModel):
    email: str
    password: str


class CurrentUserDTO(BaseModel):
    user_id: int
    email: str
