import os
import tempfile
import shutil
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def get_vector_store(persist_directory: str = None, reset: bool = False):
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if persist_directory is None:
        # Always use a unique, writable temp directory
        persist_directory = tempfile.mkdtemp(prefix="chroma_store_")

    if reset and os.path.exists(persist_directory):
        shutil.rmtree(persist_directory)

    os.makedirs(persist_directory, exist_ok=True)

    return Chroma(
        embedding_function=embedding,
        persist_directory=persist_directory
    )
