from passlib.context import CryptContext
from .base import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
import jwt
from config.environment import secret



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class UserModel(BaseModel):

  __tablename__ = "user"

  id = Column(Integer, primary_key=True, index=True)

  username = Column(String, unique=True)
  email = Column(String, unique=True)
  password = Column(String, nullable=True)

  # RELATIONSHIPS
  games = relationship('GameModel', back_populates='user', cascade="all, delete-orphan")
  reviews = relationship('ReviewModel', back_populates='user', cascade="all, delete-orphan")


  # INSTANCE METHODS

  def set_password(self, password: str):
    self.password = pwd_context.hash(password)

  def verify_password(self, password:str) -> bool:
    return pwd_context.verify(password, self.password)

  def generate_token(self):
        # Define the payload
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=1),  # Expiration time (1 day)
            "iat": datetime.now(timezone.utc),  # Issued at time
            "sub": str(self.id),  # Subject - the user ID
            "username": self.username,

        }

        # Create the JWT token
        token = jwt.encode(payload, secret, algorithm="HS256")

        return token