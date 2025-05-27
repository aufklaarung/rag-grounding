from flask import Flask, render_template, request, jsonify
from src.services.conversation import ConversationService

app = Flask(__name__)

# Initialise la collection et le service
collection_name = "tiktokdb"
conversation = ConversationService(collection_name=collection_name)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "Pas de message reçu."}), 400

    try:
        response_text = conversation.ask(user_input)
        return jsonify({"response": response_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)