from fastapi import APIRouter, Depends, HTTPException

# SQL Alchemy
from sqlalchemy.orm import Session
from models.review import ReviewModel
from models.game import GameModel

# Serializers
from serializers.review import ReviewSchema, ReviewCreateSchema, ReviewUpdateSchema

# Database Connection
from typing import List

# Middleware
from database import get_db

router = APIRouter()