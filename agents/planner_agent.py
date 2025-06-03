from agents.ingest_agent import ingest
from agents.retriever_agent import retrieve
from agents.qa_agent import answer_question

def run_pipeline(pdf_url, question, vector_store, chat_history):
    # print("[PlannerAgent] Starting pipeline")
    ingest(pdf_url, vector_store)
    docs = retrieve(question, vector_store)
    answer = answer_question(question, docs, chat_history)
    print("[PlannerAgent] Final Answer:\n", answer)
