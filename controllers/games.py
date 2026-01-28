from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.game import GameModel
from models.user import UserModel
from serializers.game import GameSchema, CreateGameSchema, UpdateGameSchema
from typing import List
from database import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()

#  Get all data
@router.get("/games", response_model=List[GameSchema])
def get_games(db: Session = Depends(get_db)):
    return db.query(GameModel).all()

# Get One data (Details)
@router.get("/games/{game_id}", response_model=GameSchema)
def get_single_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(GameModel).filter(GameModel.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game

# Create a Game
@router.post("/games", response_model=GameSchema)
def create_game(game: CreateGameSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    new_game = GameModel(**game.dict(), user_id=current_user.id)
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game


# Edit the Game
@router.put("/games/{game_id}", response_model=GameSchema)
def update_game(game_id: int, game: UpdateGameSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_game = db.query(GameModel).filter(GameModel.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    
    #  If game in database not same the user can not edit
    if db_game.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied: You are not the owner of this game")

    for key, value in game.dict().items():
        setattr(db_game, key, value)
    
    db.commit()
    db.refresh(db_game)
    return db_game


# Delete the game you choose
@router.delete("/games/{game_id}")
def delete_game(game_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_game = db.query(GameModel).filter(GameModel.id == game_id).first()

    # If not the choose game inside the database
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    
        #  If game in database not same the user can not delete

    if db_game.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied: You are not the owner of this game")

    db.delete(db_game)
    db.commit()
    return {"message": "Game deleted successfully"}