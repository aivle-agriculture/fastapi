import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PDF_DIR = os.getenv("PDF_DIR", os.path.join(BASE_DIR, "pdfs"))

def load_and_split_pdfs():
    docs = []
    for fname in os.listdir(PDF_DIR):
        if fname.lower().endswith("_약관.pdf"):
            pages = PyPDFLoader(os.path.join(PDF_DIR, fname)).load()
            for p in pages:
                p.metadata["source"] = fname
                p.metadata["items"]  = fname.replace("_약관.pdf", "")
            docs.extend(pages)
    splitter = RecursiveCharacterTextSplitter(chunk_size=350, chunk_overlap=50)
    return splitter.split_documents(docs)