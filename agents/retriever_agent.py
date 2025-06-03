def retrieve(query, vector_store):
    # print("[RetrieverAgent] Searching vector DB")
    return vector_store.similarity_search(query, k=3)
