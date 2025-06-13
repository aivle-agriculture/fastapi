from fastapi import FastAPI
from app.api.chatbot_api import router as chatbot_router

app = FastAPI()
app.include_router(chatbot_router)
