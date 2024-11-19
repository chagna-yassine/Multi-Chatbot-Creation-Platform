from app.database import engine, Base
from app.routes import auth, chatbot
from fastapi import FastAPI

# Initialize FastAPI app
app = FastAPI()

# Import models to create tables
from app.models.user import User

# Create tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(auth.router)
app.include_router(chatbot.router)
