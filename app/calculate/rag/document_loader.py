import os
from langchain_community.document_loaders import TextLoader
from app.calculate.enums import InsuredItem
from langchain.text_splitter import RecursiveCharacterTextSplitter

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PDF_DIR = os.getenv("PDF_DIR", os.path.join(BASE_DIR, "pdfs"))

def load_documents(insured_item: InsuredItem):
    match insured_item:
        case InsuredItem.FIELD_CROPS:
            loader = TextLoader(os.path.join(PDF_DIR, "calculate_field_crops_insurance.txt"))
        case InsuredItem.FRUIT_CROPS:
            loader = TextLoader(os.path.join(PDF_DIR, "calculate_fruit_crops_insurance.txt"))
        case InsuredItem.HORTICULTURAL_FACILITY:
            loader = TextLoader(os.path.join(PDF_DIR, "calculate_horticultural_facility_insurance.txt"))
        case InsuredItem.PADDY_CEREALS:
            loader = TextLoader(os.path.join(PDF_DIR, "calculate_paddy_cereals_insurance.txt"))
        case InsuredItem.MUSHROOMS:
            loader = TextLoader(os.path.join(PDF_DIR, "calculate_mushrooms_insurance.txt"))
        case _:
            raise ValueError(f"Unknown insured item: {insured_item}")

    docs = loader.load()
    return split_documents(docs)

def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,  
        chunk_overlap=50,  
        length_function=len,  
        separators=["\n\n"]  
    )
    return splitter.split_documents(docs)