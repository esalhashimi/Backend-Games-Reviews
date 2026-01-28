from pydantic import BaseModel
from typing import Optional, List
from .user import UserSchema
from .review import ReviewSchema


# start run 
class GameSchema(BaseModel):
    id: int
    name: str
    gender: str
    image: str
    description: str
    publisher: str
    rate: float
    is_released: bool
    user_id: int
    user: UserSchema
    reviews: List[ReviewSchema] = []

    class Config:
        orm_mode = True

# After Create Game
class CreateGameSchema(BaseModel):
    name: str
    gender: str
    image: str
    description: str
    publisher: str
    rate: float
    is_released: bool

    class Config:
        orm_mode = True


# After Edit the game
class UpdateGameSchema(BaseModel):
    name: str
    gender: str
    image: str
    description: str
    publisher: str
    rate: float
    is_released: bool

    class Config:
        orm_mode = True