from app import conversation
from src.extraction.sources import extract_documents
from src.embedding.ingestion import safe_add_to_chromadb
from src.clients.chromadb_client import reset_chromadb
from src.services.conversation import ConversationService
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    """
    collection_name = "relativitydb"

    # Extracting documents
    urls=["https://en.wikipedia.org/wiki/Special_relativity",
          "https://en.wikipedia.org/wiki/Spacetime",
          "https://en.wikipedia.org/wiki/Classical_mechanics",
          "https://en.wikipedia.org/wiki/Annus_mirabilis_papers",
          "https://en.wikipedia.org/wiki/Michelson%E2%80%93Morley_experiment",
          "https://en.wikipedia.org/wiki/Aether_theories",
          "https://en.wikipedia.org/wiki/Lorentz_ether_theory",
          "https://en.wikipedia.org/wiki/Hermann_Minkowski",
          "https://en.wikipedia.org/wiki/Galileo_Galilei",
          "https://en.wikipedia.org/wiki/Principle_of_relativity",
          "https://en.wikipedia.org/wiki/General_relativity",
          "https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation",
          "https://en.wikipedia.org/wiki/Philosophi%C3%A6_Naturalis_Principia_Mathematica",
          "https://en.wikipedia.org/wiki/Gravity",
          "https://en.wikipedia.org/wiki/Albert_Einstein"
          ]

    documents = []
    for url in urls:
        document = extract_documents(source='wikipedia', url=url)
        documents.extend(document)

    documents = extract_documents(source='gcs', bucket_name='mwm-cb-workspace', prefix="tiktok/html/generated/original", suffix='.html')
    safe_add_to_chromadb(documents, collection_name)
    """

    keywords = ['CapCut', '剪映']  # Latin and Chinese names

