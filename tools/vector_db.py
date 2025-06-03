# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

import os

def get_vector_store(persist_directory: str = "chroma_store"):
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Create or load Chroma vector store
    vector_store = Chroma(
        embedding_function=embedding,
        persist_directory=persist_directory
    )
    
    return vector_store

