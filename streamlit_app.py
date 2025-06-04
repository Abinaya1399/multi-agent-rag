import streamlit as st
import uuid
from tools.vector_db import get_vector_store
from tools.pdf_loader import load_pdf_from_file
from langchain.text_splitter import CharacterTextSplitter
from agents.retriever_agent import retrieve
from agents.qa_agent import answer_question

import warnings
warnings.filterwarnings("ignore", message=".*torch.classes.*")


st.set_page_config(page_title="AI PDF Chat", page_icon="📄")

st.title("📄 PDF InsightBot")
st.markdown("Start asking questions. The app remembers your chat history too!")

# Initialize session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = get_vector_store()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

# Track previous file name in session state
if "last_uploaded_file_name" not in st.session_state:
    st.session_state.last_uploaded_file_name = None    

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf", key=st.session_state.get("file_uploader_key", "default"))

# If a new file is uploaded, reset everything
if uploaded_file and uploaded_file.name != st.session_state.last_uploaded_file_name:
    st.session_state.chat_history = []  # Reset chat
    st.session_state.pdf_loaded = False  # Reset PDF load status
    st.session_state.vector_store = get_vector_store(reset=True)  # Fresh vector DB
    st.session_state.last_uploaded_file_name = uploaded_file.name  # Track new file name

if uploaded_file and not st.session_state.pdf_loaded:
    with st.spinner("Processing PDF..."):
        try:
            text = load_pdf_from_file(uploaded_file)
            chunks = CharacterTextSplitter(chunk_size=300, chunk_overlap=50).split_text(text)
            st.session_state.vector_store.add_texts(chunks)
            st.session_state.pdf_loaded = True
            st.session_state.last_uploaded_filename = uploaded_file.name
            st.success("✅ PDF successfully indexed! You can now ask questions.")
        except Exception as e:
            st.error(f"❌ Failed to process PDF: {e}")

# Chat Input and Response
if st.session_state.pdf_loaded:
    question = st.chat_input("Ask a question about the PDF...")

    if question:
        try:
            docs = retrieve(question, st.session_state.vector_store)
            answer = answer_question(question, docs, st.session_state.chat_history)
            st.session_state.chat_history.append({
                "user": question,
                "assistant": answer
            })
        except Exception as e:
            st.session_state.chat_history.append({
                "user": question,
                "assistant": f"Error: {e}"
            })

# Render chat history
for turn in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(turn["user"])
    if turn["assistant"]:
        with st.chat_message("assistant"):
            st.markdown(turn["assistant"])

# 🔁 Upload New PDF (Full Reset)
st.divider()
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []

with col2:
    if st.button("📤 Upload New PDF"):
        st.session_state.chat_history = []
        st.session_state.pdf_loaded = False
        st.session_state.vector_store = get_vector_store(reset=True)
        st.session_state.last_uploaded_file_name = None
        st.session_state.file_uploader_key = str(uuid.uuid4())  # force re-render
        st.rerun()







