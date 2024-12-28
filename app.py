from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

INTENTS = {
    "greet": ["hello", "hi", "hey"],
    "goodbye": ["bye", "goodbye", "see you"],
    "thanks": ["thanks", "thank you"]
}

@app.route("/")
def home():
    return send_file("files/index.html")

# Chat API
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()
    for intent, keywords in INTENTS.items():
        if any(keyword in user_message for keyword in keywords):
            if intent == "greet":
                return jsonify({"reply": "Hello! I am Chatbot, how can I help you?"})
            elif intent == "goodbye":
                return jsonify({"reply": "Goodbye! Have a great day!"})
            elif intent == "thanks":
                return jsonify({"reply": "You're welcome!"})

    return jsonify({"reply": "I'm sorry, I don't understand that."})

if __name__ == "__main__":
    app.run(debug=True)
