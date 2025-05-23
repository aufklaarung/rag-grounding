from src.extraction.sources import extract_documents
from src.embedding.ingestion import  safe_add_to_chromadb
from src.clients.chromadb_client import reset_chromadb
from src.services.conversation import ConversationService

import logging

if __name__ == "__main__":
    collection_name = "relativitydb"
    """
    # Extracting documents and adding to ChromaDB

    ## Extract documents from various sources
    documents = extract_documents(source='url', url="https://fr.wikipedia.org/wiki/Relativit%C3%A9_restreinte", max_paragraphs=100)
    #documents = extract_documents(source="gcs", bucket_name="mwm-cb-workspace",
    #                              prefix="tiktok/html/generated/original/", suffix=".html",
    #                              max_docs=100)
    ## Add these documents (embedded) to our vector database
    safe_add_to_chromadb(documents, collection_name)
    """
    # Initializing
    conversation = ConversationService(collection_name=collection_name)

    print("Bienvenue dans votre assistant conversationnel. Tapez 'exit' pour quitter.\n")

    while True:
        question = input("Vous: ").strip()
        if question.lower() in {"exit", "quit"}:
            print("Assistant: Au revoir !")
            break

        response = conversation.ask(question)
        print("\nAssistant:\n" + response + "\n")
