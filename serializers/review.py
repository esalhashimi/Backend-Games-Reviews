from pydantic import BaseModel
from .user import UserSchema

class ReviewSchema(BaseModel):
  id: int
  content: str
  user_id: int
  user: UserSchema

  class Config:
    orm_mode = True

class ReviewCreateSchema(BaseModel):
  content: str

  class Config:
    orm_mode = True

class ReviewUpdateSchema(BaseModel):
  content: str

  class Config:
    orm_mode = True