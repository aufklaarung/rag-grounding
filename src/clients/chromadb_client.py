from chromadb import PersistentClient
import os
import shutil

#Directory for Chroma's persistent config
PERSIST_DIR = "./chroma"
#If the directory doesn't exist, we create it
os.makedirs(PERSIST_DIR, exist_ok=True)

client = PersistentClient(PERSIST_DIR)

def reset_chromadb(persist_dir: str = "./chroma"):
    """
    Deletes the ChromaDB persistence directory to reset all collections.
    """
    if os.path.exists(persist_dir):
        shutil.rmtree(persist_dir)
        print(f"ChromaDB reset: '{persist_dir}' supprimé.")
    else:
        print(f"Aucun dossier '{persist_dir}' trouvé, rien à supprimer.")