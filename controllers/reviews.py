from fastapi import APIRouter, Depends, HTTPException

# SQL Alchemy
from sqlalchemy.orm import Session
from models.review import ReviewModel
from models.game import GameModel
from models.user import UserModel
from dependencies.get_current_user import get_current_user

# Serializers
from serializers.review import ReviewSchema, ReviewCreateSchema, ReviewUpdateSchema

# Database Connection
from typing import List

# Middleware
from database import get_db

router = APIRouter()


@router.get("/games/{game_id}/reviews", response_model=List[ReviewSchema])
def get_reviews_for_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(GameModel).filter(GameModel.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game.reviews


@router.get("/games/{game_id}/reviews/{review_id}", response_model=ReviewSchema)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review




@router.post("/games/{game_id}/reviews", response_model=ReviewSchema)
def create_review(game_id: int, review: ReviewCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    game = db.query(GameModel).filter(GameModel.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="game not found")

    new_review = ReviewModel(**review.dict(), game_id=game_id, user_id=current_user.id)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@router.put("/games/{game_id}/reviews/{review_id}", response_model=ReviewSchema)
def update_review(review_id: int, review: ReviewUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation forbidden")

    review_data = review.dict(exclude_unset=True)
    for key, value in review_data.items():
        setattr(db_review, key, value)

    db.commit()
    db.refresh(db_review)
    return db_review



@router.delete("/games/{game_id}/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    

    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Operation forbidden")

    db.delete(db_review)
    db.commit()
    return {"message": f"Review with ID {review_id} has been deleted"}
