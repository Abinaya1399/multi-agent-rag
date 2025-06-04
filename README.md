# 🤖  PDF InsightBot - A Multi-Agent RAG Chatbot

This project is a multi-agent **Retrieval-Augmented Generation (RAG)** chatbot built using **LangChain**, **Groq (LLaMA 3)**, **Chroma vector database**, and **HuggingFace sentence-transformers**. It allows you to upload or link a PDF and ask natural language questions about its contents — with multi-turn memory and clean context management.

### 🚀 Features

- 📄 Upload a PDF and start chatting
- 🧹 Clear chat or fully reset session on new upload
- 🔁 PDF re-upload creates a clean session (no stale context)
- 🔍 PDF ingestion and chunking
- 🧠 Embedding storage in Chroma vector DB
- 🤖 LLM-powered answers via Groq LLaMA3-70B
- 💬 Multi-turn chat with contextual memory
- ✅ Token-aware prompt construction
- 🔒 File uploader uses random keys to enforce reset

---

## 🔧 What It Does

- Loads a PDF from a URL
- Splits it into overlapping text chunks
- Converts each chunk to embeddings using HuggingFace
- Stores them in Chroma vector store
- Uses Groq’s LLaMA 3 model to answer your questions
- Maintains chat history for context
- Supports a full reset when a new PDF is uploaded, ensuring no old context is reused

---

## 🧰 Tech Used

- **LangChain** – agent orchestration and tool wrapping
- **Groq (LLaMA 3)** – high-speed LLM for Q&A
- **ChromaDB** – vector database for storing embeddings
- **HuggingFace sentence-transformers** – for generating semantic embeddings
- **Tiktoken** – counts tokens to stay within limits
- **PyPDF** – extracts text from PDF
- **Streamlit** – simple and reactive front-end UI


