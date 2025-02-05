from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class UserCreate(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    status: str = "user"

class UserLogin(BaseModel):
    identifier: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id : int
    user_status : str

    

class ProductCreate(BaseModel):
    seller_id: int
    name: str
    price: float
    city: str
    stock: int


class ProductResponse(BaseModel):
    id: int
    seller: int  # ID du vendeur
    name: str
    price: float
    city: str
    stock: int

    class Config:
        orm_mode = True


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    total_price: float


class OrderResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    quantity: int
    status: str
    total_price: float

    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    product_id: int
    link: str
    description: str
    type: str = "image" # "image" ou "video"

class PostResponse(BaseModel):
    id: int
    product_id: int
    link: str
    description: str
    type: str
    product__seller_id : int

    class Config:
        orm_mode = True



class NotificationCreate(BaseModel):
    user_id: int
    title: str
    content: str

class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    status: str = "user"

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    date : datetime

class VideoFormationCreate(BaseModel):
    link : str
    user_id: int
    description : str
    type : str = "video"  # "texte" ou "video"


class TextFormationCreate(BaseModel):
    user_id: int
    type : str = "texte"  # "texte" ou "video"
    content : str
    user_id: int

class FormationResponse(BaseModel):
    id: int
    user_id: int
    content: str
    link : str
    description : str
    type : str
    date : datetime