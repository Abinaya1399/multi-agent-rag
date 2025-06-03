# from langchain_groq import ChatGroq
# from langchain.schema import HumanMessage

# llm = ChatGroq(temperature=0, model="llama3-70b-8192")

# def answer_question(query, context_docs):
#     context = "\n\n".join([doc.page_content for doc in context_docs])
#     prompt = f"Context:\n{context}\n\nQuestion: {query}"
#     return llm.invoke([HumanMessage(content=prompt)]).content

# from langchain_groq import ChatGroq
# from langchain.schema import HumanMessage
# from transformers import AutoTokenizer

# # Initialize Groq LLM and tokenizer
# llm = ChatGroq(temperature=0, model="llama3-70b-8192")
# tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")  # lightweight tokenizer
# # tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3-8b-hf")

# MAX_TOKENS = 6000
# RESERVED_FOR_PROMPT_AND_QUESTION = 500

# def count_tokens(text):
#     return len(tokenizer.encode(text, truncation=True, max_length=512))

# def answer_question(query, context_docs):
#     context = ""
#     total_tokens = 0
#     allowed_tokens = MAX_TOKENS - RESERVED_FOR_PROMPT_AND_QUESTION

#     for doc in context_docs:
#         chunk = doc.page_content
#         chunk_tokens = count_tokens(chunk)

#         if total_tokens + chunk_tokens > allowed_tokens:
#             break

#         context += chunk + "\n\n"
#         total_tokens += chunk_tokens

#     prompt = f"Context:\n{context}\n\nQuestion: {query}"
#     return llm.invoke([HumanMessage(content=prompt)]).content

# from langchain_groq import ChatGroq
# from langchain.schema import HumanMessage
# from transformers import AutoTokenizer

# # Initialize Groq LLM and tokenizer
# llm = ChatGroq(temperature=0, model="llama3-70b-8192")
# tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")  # lightweight tokenizer

# MAX_TOKENS = 6000
# RESERVED_FOR_PROMPT_AND_QUESTION = 500
# CHUNK_LIMIT = 512  # max tokens per chunk

# def truncate_chunk(text):
#     tokens = tokenizer.encode(text, truncation=True, max_length=CHUNK_LIMIT)
#     return tokenizer.decode(tokens, skip_special_tokens=True)

# def count_tokens(text):
#     return len(tokenizer.encode(text))

# def answer_question(query, context_docs):
#     context = ""
#     total_tokens = 0
#     allowed_tokens = MAX_TOKENS - RESERVED_FOR_PROMPT_AND_QUESTION

#     for doc in context_docs:
#         chunk = truncate_chunk(doc.page_content)
#         chunk_tokens = count_tokens(chunk)

#         if total_tokens + chunk_tokens > allowed_tokens:
#             break

#         context += chunk + "\n\n"
#         total_tokens += chunk_tokens

#     prompt = f"Context:\n{context}\n\nQuestion: {query}"
#     return llm.invoke([HumanMessage(content=prompt)]).content

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, AIMessage
import tiktoken

# Initialize Groq LLM
llm = ChatGroq(temperature=0, model="llama3-70b-8192")

# Token limits
MAX_TOKENS = 6000
RESERVED_FOR_PROMPT_AND_QUESTION = 500
allowed_tokens = MAX_TOKENS - RESERVED_FOR_PROMPT_AND_QUESTION

# Tokenizer that overestimates slightly for safety
tokenizer = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(tokenizer.encode(text))

def answer_question(query, context_docs, chat_history):
    context = ""
    total_tokens = 0

    for doc in context_docs:
        chunk = doc.page_content
        chunk_tokens = count_tokens(chunk)
        if total_tokens + chunk_tokens > allowed_tokens:
            break
        context += chunk + "\n\n"
        total_tokens += chunk_tokens

    # Chat history (only valid strings)
    messages = []
    for turn in chat_history:
        user_msg = turn.get("user")
        assistant_msg = turn.get("assistant")
        if isinstance(user_msg, str):
            messages.append(HumanMessage(content=user_msg))
        if isinstance(assistant_msg, str):
            messages.append(AIMessage(content=assistant_msg))

    prompt = f"Context:\n{context}\n\nQuestion: {query}"
    prompt_tokens = count_tokens(prompt)

    if prompt_tokens > MAX_TOKENS:
        raise ValueError(f"Prompt still too large: {prompt_tokens} tokens")

    messages.append(HumanMessage(content=prompt))

    try:
        response = llm.invoke(messages)
        response_text = response.content or "⚠️ No answer returned."
    except Exception as e:
        response_text = f"⚠️ LLM invocation failed: {str(e)}"

    # Save to history
    chat_history.append({
        "user": query,
        "assistant": response_text
    })

    return response_text


    # return llm.invoke([HumanMessage(content=prompt)]).content






