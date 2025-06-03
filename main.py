from tools.vector_db import get_vector_store
from agents.planner_agent import run_pipeline

# if __name__ == "__main__":
    # url = input("Enter PDF URL: ").strip()
    # question = input("Ask a question: ").strip()
    # vector_store = get_vector_store()
    # run_pipeline(url, question, vector_store)

    # Initialize vector DB once
    # Initialize vector DB once
vector_store = get_vector_store()

# Step 1: Ask for the PDF URL once
pdf_url = input("Enter PDF URL: ").strip()
chat_history = []  # Stores user & assistant messages

# Step 2: Ask questions in a loop
while True:
    question = input("Ask a question (or type 'exit' to quit): ").strip()
    
    if question.lower() in ["exit", "quit", "i'm done", "done"]:
        print("Session ended. Goodbye!")
        break
    run_pipeline(pdf_url, question, vector_store, chat_history)

#https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf

