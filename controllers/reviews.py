from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.review import ReviewModel
from models.game import GameModel
from models.user import UserModel
from serializers.review import ReviewSchema, ReviewCreateSchema, ReviewUpdateSchema
from database import get_db
from dependencies.get_current_user import get_current_user
from typing import List

router = APIRouter()

# 1. Get all reviews for a specific game
@router.get("/games/{game_id}/reviews", response_model=List[ReviewSchema])
def get_reviews_for_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(GameModel).filter(GameModel.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game.reviews

# 2. Get a single review by ID
@router.get("/games/{game_id}/reviews/{review_id}", response_model=ReviewSchema)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

# 3. Create a new review (Authenticated)
@router.post("/games/{game_id}/reviews", response_model=ReviewSchema)
def create_review(game_id: int, review: ReviewCreateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    game = db.query(GameModel).filter(GameModel.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    new_review = ReviewModel(**review.dict(), game_id=game_id, user_id=current_user.id)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

# 4. Update a review (Owner Only)
@router.put("/games/{game_id}/reviews/{review_id}", response_model=ReviewSchema)
def update_review(review_id: int, review: ReviewUpdateSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # Check Ownership
    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission Denied: You can only update your own reviews")

    review_data = review.dict(exclude_unset=True)
    for key, value in review_data.items():
        setattr(db_review, key, value)

    db.commit()
    db.refresh(db_review)
    return db_review

# 5. Delete a review (Owner Only)
@router.delete("/games/{game_id}/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    
    # CRITICAL: Check if the logged-in user is the one who wrote the review
    if db_review.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission Denied: You can only delete your own reviews")

    db.delete(db_review)
    db.commit()
    return {"message": f"Review with ID {review_id} has been successfully deleted"}