import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from models.game import GameModel
from models.user import UserModel
from serializers.game import GameSchema
from typing import List, Optional
from database import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()

UPLOAD_DIR = "static/images"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

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
async def create_game(
    name: str = Form(...),
    gender: str = Form(...),
    description: str = Form(...),
    publisher: str = Form(...),
    rate: float = Form(...),
    is_released: bool = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{image.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    new_game = GameModel(
        name=name,
        gender=gender,
        description=description,
        publisher=publisher,
        rate=rate,
        is_released=is_released,
        image=file_path,
        user_id=current_user.id
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game

@router.put("/games/{game_id}", response_model=GameSchema)
async def update_game(
    game_id: int, 
    name: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    publisher: Optional[str] = Form(None),
    rate: Optional[float] = Form(None),
    is_released: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    db_game = db.query(GameModel).filter(GameModel.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")
    if db_game.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permission Denied")

    update_data = {"name": name, "gender": gender, "description": description, 
                   "publisher": publisher, "rate": rate, "is_released": is_released}
    
    for key, value in update_data.items():
        if value is not None:
            setattr(db_game, key, value)

    if image:
        file_path = os.path.join(UPLOAD_DIR, f"{current_user.id}_{image.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        db_game.image = file_path

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
    
    if db_game.image and os.path.exists(db_game.image):
        os.remove(db_game.image)

    db.delete(db_game)
    db.commit()
    return {"message": f"Game with id {game_id} was deleted!"}