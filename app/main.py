from fastapi import FastAPI
# from app.api.chatbot_api import router as chatbot_router
from app.api.calculate_api import router as calculate_router
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# app.include_router(chatbot_router, prefix="/api")
app.include_router(calculate_router, prefix="/api")
