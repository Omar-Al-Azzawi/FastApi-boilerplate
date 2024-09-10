from fastapi import FastAPI
from app.models.users import User
from app.routes.users import router as user_routes
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine

# Create tables
User.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes, prefix="/users", tags=["users"])