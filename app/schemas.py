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

    

class ProductCreate(BaseModel):
    seller_id: int
    name: str
    price: float
    city: str
    stock: int


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    total_price: float


class PostCreate(BaseModel):
    product_id: int
    link: str
    description: str
    type: str  # "image" ou "video"

class PostResponse(BaseModel):
    id: int
    product_id: int
    link: str
    description: str
    type: str

    class Config:
        orm_mode = True
