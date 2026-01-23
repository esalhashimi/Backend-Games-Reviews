from .base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class ReviewModel(BaseModel):
    __tablename__ = "Reviews"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)


     # relationships
    game_id = Column(Integer, ForeignKey("Games.id", ondelete="CASCADE"), nullable=False)
    game = relationship("GameModel", back_populates = "reviews", passive_deletes=True)

    user_id = Column(Integer, ForeignKey('users.id',  ondelete="CASCADE"), nullable=False)
    user = relationship('UserModel', back_populates='reviews')