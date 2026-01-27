from .base import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship


class GameModel(BaseModel):

    # TABLE in Postgresql
    __tablename__ = "Game"

    id = Column(Integer, primary_key=True, index=True)

    # Specific columns for our Game Table.
    name = Column(String, unique=True)
    gender = Column(String)
    image = Column(String)
    description = Column(String)
    publisher = Column(String)
    rate = Column(Float)
    is_released = Column(Boolean)

    # Relationships
    reviews = relationship ("ReviewModel", back_populates="game", cascade="all, delete-orphan")

    user_id = Column(Integer, ForeignKey('users.id',  ondelete="CASCADE"), nullable=False)
    user = relationship('UserModel', back_populates='games')