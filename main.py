from src.services.conversation import ConversationService

if __name__ == "__main__":
    collection_name = "tiktokdb"
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
