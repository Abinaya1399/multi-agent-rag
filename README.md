# 🤖 Multi-Agent RAG Chatbot (PDF Q&A)

This project is a multi-agent **Retrieval-Augmented Generation (RAG)** chatbot built using **LangChain**, **Groq (LLaMA 3)**, **Chroma vector database**, and **HuggingFace sentence-transformers**. It allows you to upload or link a PDF and ask natural language questions about its contents.

### 🚀 Features

- 🔍 PDF ingestion and chunking
- 🧠 Embedding storage in a vector database (Chroma)
- 🤖 LLM-powered Q&A using Groq's LLaMA3-70B
- 🧠 Contextual multi-turn conversation
- ✅ Token-efficient prompt construction
- 💬 Conversational history memory

---

## 🔧 What It Does

- Loads a PDF from a URL
- Splits it into smaller chunks
- Converts text chunks into vector embeddings
- Stores them in a vector database (Chroma)
- Uses Groq’s LLaMA 3 model to answer your questions
- Remembers past questions for context

---

## 🧰 Tech Used

- **LangChain** – connects everything together
- **Groq (LLaMA 3)** – large language model for answering
- **ChromaDB** – vector database for storing embeddings
- **HuggingFace Transformers** – for generating embeddings
- **Tiktoken** – counts tokens to stay within limits
- **PyPDF** – extracts text from PDF


