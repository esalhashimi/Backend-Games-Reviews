from pydantic import BaseModel
from .user import UserSchema


# Start run
class ReviewSchema(BaseModel):
  id: int
  content: str
  user_id: int
  user: UserSchema

  class Config:
    orm_mode = True


# After Create Review
class ReviewCreateSchema(BaseModel):
  content: str

  class Config:
    orm_mode = True


# After Edit the Review
class ReviewUpdateSchema(BaseModel):
  content: str

  class Config:
    orm_mode = True