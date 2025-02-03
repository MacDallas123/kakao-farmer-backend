from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    status: str = "user"

class Token(BaseModel):
    access_token: str
    token_type: str

