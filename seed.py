from sqlalchemy import create_engine
from config.environment import db_URI
from sqlalchemy.orm import  sessionmaker
from models.base import Base
from models.user import UserModel
from models.game import GameModel
from models.review import ReviewModel
from data.user_data import user_list
from data.game_data import games_list
from data.review_data import reviews_list


engine = create_engine(db_URI)
SessionLocal = sessionmaker(bind=engine)

try:
    print("Recreating database...")
    # Drop and recreate tables to ensure a clean slate
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("Seeding the database...")
    db = SessionLocal()

    db.add_all(user_list)
    db.commit()

    # Seed games
    db.add_all(games_list)
    db.commit()

    # Seed reviews
    db.add_all(reviews_list)
    db.commit()
    db.close()

    print("Database seeding complete! 👋")
except Exception as e:
    print("An error occurred:", e)