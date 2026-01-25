
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.game import GameModel
from models.user import UserModel
from serializers.game import GameSchema, CreateGameSchema, UpdateGameSchema
from typing import List
from database import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()



@router.get("/games", response_model=List[GameSchema])
def get_games(db: Session = Depends(get_db)):
    return db.query(GameModel).all()

@router.get("/games/{game_id}", response_model=GameSchema)
def get_single_game(game_id: int, db: Session = Depends(get_db)):
    game = db.query(GameModel).filter(GameModel.id == game_id).first()
    if not game:
         raise HTTPException(status_code=404, detail="Game not found")
    return game

@router.post("/games", response_model=GameSchema)
def create_game(game: CreateGameSchema,  db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    new_game = GameModel(**game.dict(), user_id=current_user.id)
    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return new_game

@router.put("/games/{game_id}", response_model=GameSchema)
def update_game(game_id: int, game: UpdateGameSchema, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_game  = db.query(GameModel).filter(GameModel.id == game_id).first()

    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")

    if db_game.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission Denied")

    game_form_data = game.dict(exclude_unset=True)

    for key, value in game_form_data.items():
        setattr(db_game, key, value)

    db.commit()
    db.refresh(db_game)

    return db_game

@router.delete("/games/{game_id}")
def delete_game(game_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    db_game = db.query(GameModel).filter(GameModel.id == game_id).first()
    if not db_game:
         raise HTTPException(status_code=404, detail="Game not found")
    if db_game.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission Denied")
    

    db.delete(db_game)
    db.commit()
    return {"message": f"Game with id {game_id} was deleted!"}