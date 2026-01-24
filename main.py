# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from controllers.games import router as GamesRouter
from controllers.reviews import router as ReviewsRouter
from controllers.users import router as UserRouter

app = FastAPI()

# Allow your React dev server(s) to call the API
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # Which sites can call this API
    allow_methods=["*"],       # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],       # Allow all headers (e.g., Content-Type, Authorization)
)


# ROUTES

app.include_router(GamesRouter, prefix="/api")
app.include_router(ReviewsRouter, prefix="/api")
app.include_router(UserRouter, prefix="/api")


@app.get("/")
def Home():
    return {"Welcome": "Hello inside Website Page Games Reviews"}