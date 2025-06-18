import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DB_DIR = os.getenv("DB_DIR", os.path.join(BASE_DIR, "chroma/calculate_db"))

def create_retriever(documents):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    return vectorstore.as_retriever()