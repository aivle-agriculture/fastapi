from .document_loader import load_documents
from .retriever_factory import create_retriever
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from app.calculate.enums import InsuredItem

async def calculate_with_rag(insured_item: InsuredItem, prompt: str) -> dict:
    docs = load_documents(insured_item)
    retriever = create_retriever(docs)
    llm = ChatOpenAI(model="gpt-4o")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False
    )

    return qa_chain.invoke(prompt)