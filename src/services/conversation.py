from typing import List, Tuple
from src.prompts.cot_prompt import build_prompt
from src.embedding.retriever import get_best_matches
from src.clients.gemini_client import get_model_response

class ConversationService:
    """
    Handles a conversation grounded in documents stored in a ChromaDB collection.

    Args:
        collection_name: The ChromaDB collection used for similarity search.
    """
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.history: List[Tuple[str, str]] = []

    def enrich_query(self, current_question: str) -> str:
        previous_questions = " ".join(q for q, _ in self.history)
        return previous_questions + " " + current_question

    def ask(self, question: str) -> str:
        enriched_query = self.enrich_query(question)
        best_passages = get_best_matches(enriched_query, self.collection_name, max_results=20)
        if not best_passages:
            return "Je n’ai trouvé aucun passage pertinent pour répondre à cette question."
        prompt = build_prompt(question, best_passages, self.history)

        response = get_model_response(prompt)
        self.history.append((question, response))
        return response