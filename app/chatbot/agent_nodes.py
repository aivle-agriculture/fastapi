from typing import Annotated, TypedDict, Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph.message import add_messages

llm = ChatOpenAI(model="gpt-4o", temperature=0)

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    documents: list

def agent_node(state):
    model = llm.bind_tools(state.get("retriever_tools", []))
    resp = model.invoke(state["messages"])
    return {"messages": [resp]}

def rewrite_node(state):
    question = state["messages"][0].content
    msg = [HumanMessage(content=f"다음 질문을 더 나은 검색어로 바꿔주세요:\n{question}")]
    resp = llm.invoke(msg)
    return {"messages": [resp]}

def generate_node(state):
    question = state["messages"][0].content
    context = "\n\n".join(doc.page_content for doc in state.get("documents", []))
    prompt = PromptTemplate.from_template(
        """당신은 보험 약관 기반 질문 응답 챗봇입니다.
        질문: {question}
        약관 발췌 내용: {context}
        응답:"""
    )
    chain = prompt | llm | StrOutputParser()
    ans = chain.invoke({"question": question, "context": context})
    return {"messages": [AIMessage(content=ans)]}

def grade_documents(state) -> Literal["generate", "rewrite"]:
    class Grade(BaseModel):
        binary_score: str = Field(...)
    question = state["messages"][0].content
    context = "\n\n".join(doc.page_content for doc in state.get("documents", []))
    prompt = PromptTemplate(
        template="""당신은 검색된 문서가 사용자 질문과 관련이 있는지 평가합니다.
문서: {context}
질문: {question}
관련 있으면 'yes', 없으면 'no'를 출력하세요.""",
        input_variables=["context", "question"]
    )
    chain = prompt | llm.with_structured_output(Grade)
    out = chain.invoke({"context": context, "question": question})
    return "generate" if out.binary_score == "yes" else "rewrite"
