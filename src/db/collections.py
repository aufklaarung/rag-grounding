# src/db/collections.py
from src.clients.chromadb_client import client
from src.embedding.embedding_function import EmbeddingFunction

def get_document_collection(name: str):
    """
    Returns a ChromaDB collection configured for document embedding.
    """
    embedding_function = EmbeddingFunction(document_mode=True)
    return client.get_or_create_collection(
        name,
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"}
    )

def get_query_collection(name: str):
    """
    Returns a ChromaDB collection configured for querying with query-mode embeddings.
    """
    embedding_function = EmbeddingFunction(document_mode=False)
    return client.get_collection(name, embedding_function=embedding_function)  # query embedding used at retrieval time only