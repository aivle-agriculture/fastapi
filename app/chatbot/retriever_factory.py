import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.tools.retriever import create_retriever_tool
from .document_loader import load_and_split_pdfs
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_DIR = os.getenv("DB_DIR", os.path.join(BASE_DIR, "chroma/policy_db"))

embedding = OpenAIEmbeddings()

def build_vectorstore(chunks):
    texts  = [c.page_content for c in chunks]
    metas  = [c.metadata     for c in chunks]
    return Chroma.from_texts(
        texts=texts,
        embedding=embedding,
        metadatas=metas,
        persist_directory=DB_DIR
    )

def setup_retriever():
    chunks = load_and_split_pdfs()
    vs = build_vectorstore(chunks)
    retriever = vs.as_retriever()
    retriever_tool = create_retriever_tool(
        retriever,
        name="retrieve_insurance_docs",
        description="농작물 재해보험 약관에서 보장 내용·보장 범위·가입 조건 등을 검색합니다."
    )
    return retriever_tool
