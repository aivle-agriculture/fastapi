from fastapi import APIRouter
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from app.chatbot.rag_workflow import graph

router = APIRouter()

class ChatRequest(BaseModel):
    conversationId: str
    context: str 
    question: str

class ChatResponse(BaseModel):
    conversationId: str
    answer: str

@router.post("/chat", response_model=ChatResponse)
async def ask(query: ChatRequest):
    messages = []
    if query.context.strip():
        for line in query.context.strip().split("\n"):
            line = line.strip()
            if line.startswith("USER:"):
                messages.append(HumanMessage(content=line.replace("USER:", "", 1).strip()))
            elif line.startswith("ASSISTANT:"):
                messages.append(AIMessage(content=line.replace("ASSISTANT:", "", 1).strip()))
    messages.append(HumanMessage(content=query.question))

    inputs = {"messages": messages}
    result = graph.invoke(inputs)

    answer = ""
    for msg in result["messages"]:
        if isinstance(msg, AIMessage) and hasattr(msg, "content"):
            answer += msg.content
    if not answer and result["messages"]:
        last_msg = result["messages"][-1]
        if hasattr(last_msg, "content"):
            answer = last_msg.content
    return {"conversationId": query.conversationId, "answer": answer}