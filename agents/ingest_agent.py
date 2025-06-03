from tools.pdf_loader import load_pdf_from_url
from langchain.text_splitter import CharacterTextSplitter

def ingest(url, vector_store):
    # print("[IngestAgent] Loading PDF")
    text = load_pdf_from_url(url)
    chunks = CharacterTextSplitter(chunk_size=300, chunk_overlap=50).split_text(text)
    # print("[IngestAgent] Storing chunks to vector store")
    vector_store.add_texts(chunks)
