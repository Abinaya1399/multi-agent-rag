from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage
import tiktoken

# Initialize Groq LLM
llm = ChatGroq(temperature=0, model="llama3-70b-8192")

# Token limits
MAX_TOKENS = 6000
RESERVED_FOR_PROMPT_AND_QUESTION = 500
ALLOWED_TOKENS = MAX_TOKENS - RESERVED_FOR_PROMPT_AND_QUESTION

# Tokenizer (approximate, overestimates for safety)
tokenizer = tiktoken.get_encoding("cl100k_base")

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

def answer_question(query, context_docs, chat_history):
    # Build the context from retrieved docs (limited by tokens)
    context = ""
    total_tokens = 0
    for doc in context_docs:
        chunk = doc.page_content
        chunk_tokens = count_tokens(chunk)
        if total_tokens + chunk_tokens > ALLOWED_TOKENS:
            break
        context += chunk + "\n\n"
        total_tokens += chunk_tokens

    # Build chat memory for continuity
    messages = []
    # if chat_history:
    for turn in chat_history:
        user_msg = turn.get("user")
        assistant_msg = turn.get("assistant")
        if isinstance(user_msg, str):
            messages.append(HumanMessage(content=user_msg))
        if isinstance(assistant_msg, str):
            messages.append(AIMessage(content=assistant_msg))

    # Append current query with fresh context
    prompt = f"Context:\n{context}\n\nQuestion: {query}"
    messages.append(HumanMessage(content=prompt))

    try:
        response = llm.invoke(messages)
        answer = response.content or "⚠️ No answer returned."
    except Exception as e:
        answer = f"⚠️ LLM invocation failed: {str(e)}"

    # # Update chat history (used by streamlit_app.py)
    # chat_history.append({
    #     "user": query,
    #     "assistant": answer
    # })

    return answer



