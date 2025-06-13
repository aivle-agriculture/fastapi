from fastapi import APIRouter
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from app.chatbot.rag_workflow import graph

router = APIRouter()

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str

@router.post("/chat", response_model=ChatResponse)
async def ask(query: ChatRequest):
    inputs = {"messages": [HumanMessage(content=query.question)]}
    result = graph.invoke(inputs)

    answer = ""
    for msg in result["messages"]:
        if isinstance(msg, AIMessage) and hasattr(msg, "content"):
            answer += msg.content
    if not answer:
        last_msg = result["messages"][-1]
        if hasattr(last_msg, "content"):
            answer = last_msg.content
    return {"answer": answer}