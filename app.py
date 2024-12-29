from flask import Flask, request, jsonify, send_file
import requests, os, random
from dotenv import load_dotenv

load_dotenv(dotenv_path="tunebot_env/.env")

app = Flask(__name__)

LASTFM_API_URL = os.getenv("LASTFM_API_URL")
API_KEY = os.getenv("API_KEY")

INTENTS = {
    "greet": ["hello", "hi", "hey"],
    "goodbye": ["bye", "goodbye", "see you"],
    "thanks": ["thanks", "thank you"],
    "mood": ["happy", "sad", "angry", "relaxed", "excited", "romantic", "energetic"]
}

MOOD_GENRES = {
    "happy": "pop",
    "sad": "acoustic",
    "angry": "rock",
    "relaxed": "chill",
    "excited": "dance",
    "romantic": "love songs",
    "energetic": "workout"
}


@app.route("/")
def home():
    return send_file("files/index.html")


def map_mood(mood):
    return MOOD_GENRES.get(mood, "pop")


def get_recommendations(genre):
    params = {
        "method": "tag.getTopTracks",
        "tag": genre,
        "api_key": API_KEY,
        "format": "json",
    }
    try:
        response = requests.get(LASTFM_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if 'tracks' in data:
            songs = data['tracks']['track']
            song_list = [{"name": song['name'], "artist": song['artist']['name']} for song in songs]
            random_songs = random.sample(song_list, 5) if len(song_list) >= 5 else song_list
            return random_songs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    return None


# Chat API
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()
    for intent, keywords in INTENTS.items():
        if any(keyword in user_message for keyword in keywords):
            if intent == "greet":
                return jsonify({
                    "reply": "Hello! I am TuneBot. Tell me your mood or what kind of music you like, and I’ll suggest some tunes!"})
            elif intent == "goodbye":
                return jsonify({"reply": "Goodbye! Have a great day!"})
            elif intent == "thanks":
                return jsonify({"reply": "You're welcome!"})
            elif intent == "mood":
                genre = map_mood(user_message)
                songs = get_recommendations(genre)

                if songs:
                    song_names = "<br>".join([f"{song['name']} by {song['artist']}" for song in songs])
                    return jsonify({"reply": f"Here are some songs for your {genre} mood:<br>{song_names}"})
                else:
                    return jsonify({"reply": "Sorry, I couldn't find any songs for that mood. Try again!"})

    return jsonify({"reply": "I'm sorry, I don't understand that."})


if __name__ == "__main__":
    app.run(debug=True)
