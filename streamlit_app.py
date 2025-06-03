import streamlit as st
from tools.vector_db import get_vector_store
from tools.pdf_loader import load_pdf_from_file
from langchain.text_splitter import CharacterTextSplitter
from agents.retriever_agent import retrieve
from agents.qa_agent import answer_question

st.set_page_config(page_title="AI PDF Chat", page_icon="📄")

st.title("📄 Chat with your PDF")
st.markdown("Upload a PDF and start asking questions. The app remembers your chat history too!")

# Initialize session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = get_vector_store()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file and not st.session_state.pdf_loaded:
    with st.spinner("Processing PDF..."):
        try:
            text = load_pdf_from_file(uploaded_file)
            chunks = CharacterTextSplitter(chunk_size=300, chunk_overlap=50).split_text(text)
            st.session_state.vector_store.add_texts(chunks)
            st.session_state.pdf_loaded = True
            st.success("✅ PDF successfully indexed! You can now ask questions.")
        except Exception as e:
            st.error(f"❌ Failed to process PDF: {e}")

# Chat input
if st.session_state.pdf_loaded:
    question = st.chat_input("Ask a question about the PDF...")

    if question:
        # Save user message in chat history
        st.session_state.chat_history.append({"user": question, "assistant": None})

        try:
            docs = retrieve(question, st.session_state.vector_store)
            answer = answer_question(question, docs, st.session_state.chat_history)
            # Save assistant response
            st.session_state.chat_history[-1]["assistant"] = answer
        except Exception as e:
            st.session_state.chat_history[-1]["assistant"] = f"Error: {e}"

# Display previous chat history (excluding last if already printed)
for turn in st.session_state.chat_history[:-1]:
    with st.chat_message("user"):
        st.markdown(turn["user"])
    if turn["assistant"]:
        with st.chat_message("assistant"):
            st.markdown(turn["assistant"])

# Display the latest interaction if needed
if st.session_state.chat_history:
    last_turn = st.session_state.chat_history[-1]
    if last_turn["assistant"]:  # Show only if answer is ready
        with st.chat_message("assistant"):
            st.markdown(last_turn["assistant"])

