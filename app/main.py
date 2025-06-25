from fastapi import FastAPI
from app.api.chatbot_api import router as chatbot_router
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(chatbot_router, prefix="/api")