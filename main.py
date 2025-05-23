from src.extraction.sources import extract_documents
from src.embedding.ingestion import  safe_add_to_chromadb
from src.embedding.retriever import  get_best_matches
from src.clients.chromadb_client import reset_chromadb

import logging

if __name__ == "__main__":
    collection_name = "test"
    # Extract documents from various sources
    documents = extract_documents(source="gcs", bucket_name="mwm-cb-workspace",
                                  prefix="tiktok/html/generated/original/", suffix=".html", max_docs=10)
    #Add these documents (embedded) to our vector database
    safe_add_to_chromadb(documents, collection_name)
    # RAG time
    results = get_best_matches("Qui est Albert Einstein?", collection_name)