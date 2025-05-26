# src/embedding/retriever.py
from typing import List
from src.db.collections import get_query_collection

def get_best_matches(
    query: str,
    collection_name: str,
    threshold: float = 0.60,
    max_results: int = 40
) -> List[str]:
    """
    Query ChromaDB using a similarity search and filter results above a threshold.
    """
    db = get_query_collection(collection_name)

    result = db.query(query_texts=[query], n_results=max_results)
    documents = result["documents"][0]
    scores = result["distances"][0]

    filtered = [doc for doc, score in zip(documents, scores) if score <= (1-threshold)]
    print(f"🔍 Retrieved {len(filtered)} matches (threshold={threshold})")
    return filtered