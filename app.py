from flask import Flask, request, jsonify, send_file
import requests, os, random, spotipy
from urllib.parse import quote
from dotenv import load_dotenv
import spacy

load_dotenv(dotenv_path="tunebot_env/.env")
app = Flask(__name__)

DEEZER_API_URL = "https://api.deezer.com"

INTENTS = {
    "greet": ["hello", "hi", "hey", "hola"],
    "goodbye": ["bye", "goodbye", "see you"],
    "thanks": ["thanks", "thank you"],
    "no": ["no", "nope"]
    # "mood": ["happy", "sad", "angry", "relaxed", "excited", "romantic", "energetic"]
}

MOOD_GENRES = {
    "happy": "pop",
    "sad": "acoustic",
    "angry": "rock",
    "relaxed": "chill",
    "excited": "dance",
    "romantic": "love songs",
    "energetic": "workout",
    "calm": "classical",
    "motivated": "hip-hop",
    "nostalgic": "oldies",
    "melancholy": "indie",
    "adventurous": "indie rock",
    "party": "EDM",
    "chill": "lo-fi"
}

mood_keywords = {
    "happy": ["happy", "joyful", "excited", "good", "cheerful", "elated"],
    "sad": ["sad", "down", "blue", "unhappy", "mournful", "gloomy"],
    "angry": ["angry", "furious", "mad", "upset", "irritated"],
    "relaxed": ["relaxed", "calm", "chill", "peaceful", "serene"],
    "romantic": ["romantic", "love", "affection", "heart", "sweet", "passionate", "adoring"],
    "energetic": ["energetic", "active", "lively", "vibrant", "bouncy"],
    "calm": ["calm", "peaceful", "serene", "tranquil", "soothing"],
    "motivated": ["motivated", "inspired", "focused", "determined", "ambitious"],
    "nostalgic": ["nostalgic", "retro", "throwback", "old", "vintage", "memory"],
    "melancholy": ["melancholy", "reflective", "lonely", "nostalgic", "pensive"],
    "adventurous": ["adventurous", "exploring", "curious", "wild", "free", "daring"],
    "party": ["party", "celebration", "fun", "dance", "club", "festive"],
    "chill": ["chill", "relax", "laid-back", "smooth", "mellow", "cozy"]
}

nlp = spacy.load("en_core_web_sm")


@app.route("/")
def home():
    return send_file("files/index.html")


def get_spotify_token():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        print("Error: Missing Spotify credentials.")
        return None

    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    body = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(url, headers=headers, data=body)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Error fetching token: {response.status_code} - {response.text}")
        return None


def get_spotify_link(song_name, artist_name):
    try:
        token = get_spotify_token()
        if not token:
            print("Error: Could not get Spotify token.")
            return None

        headers = {"Authorization": f"Bearer {token}"}

        query = f"track:{song_name} artist:{artist_name}"
        url = f"https://api.spotify.com/v1/search?q={quote(query)}&type=track&limit=1"
        response = requests.get(url, headers=headers)
        data = response.json()

        if not data.get("tracks", {}).get("items"):
            url = f"https://api.spotify.com/v1/search?q={quote(song_name)}&type=track&limit=5"
            response = requests.get(url, headers=headers)
            data = response.json()

            for item in data.get("tracks", {}).get("items", []):
                for artist in item.get("artists", []):
                    if artist_name.lower() in artist["name"].lower():
                        return item["external_urls"]["spotify"]
            return None

        return data["tracks"]["items"][0]["external_urls"]["spotify"]

    except Exception as e:
        print(f"Error fetching Spotify link: {e}")
    return None


def get_recommendations(genre):
    search_url = f"{DEEZER_API_URL}/search"
    params = {"q": genre.lower()}
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        if 'data' in data:
            songs = data['data']
            song_list = []
            for song in songs:
                song_name = song['title']
                artist_name = song['artist']['name']

                song_list.append({
                    "name": song_name,
                    "artist": artist_name,
                    "deezer_link": song['link']
                })

            # Return up to 5 random songs
            random_songs = random.sample(song_list, 5) if len(song_list) >= 5 else song_list
            return random_songs
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    return None


# Chat API
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").lower()

    doc = nlp(user_message.lower())
    genre = None
    user_mood = None

    asking_mood = False

    for mood, keywords in mood_keywords.items():
        for keyword in keywords:
            if keyword in doc.text:
                user_mood = keyword
                genre = MOOD_GENRES.get(mood)
                asking_mood = True
                break
        if user_mood:
            asking_mood = True
            break

    if not asking_mood:
        for intent, keywords in INTENTS.items():
            if any(keyword in user_message for keyword in keywords):
                if intent == "greet":
                    return jsonify({
                        "reply": "🎵 Hi there! I'm TuneBot. Tell me your mood, and I'll recommend some tunes!"})
                elif intent == "goodbye":
                    return jsonify({"reply": "👋 Goodbye! Have a great day!"})
                elif intent == "thanks":
                    return jsonify({"reply": "😊 You're welcome!"})
                elif intent == "no":
                    return jsonify({"reply": "😔 Pretty Please"})

    if not genre:
        return jsonify({"reply": "I couldn't detect your mood. Could you tell me more?"})

    songs = get_recommendations(genre)

    if songs:
        song_names = ""
        for song in songs:
            spotify_link = get_spotify_link(song['name'], song['artist'])
            deezer_link = song.get('deezer_link')
            if spotify_link:
                link = spotify_link
                platform = "Spotify"
            elif deezer_link:
                link = deezer_link
                platform = "Deezer"
            else:
                continue

            song_names += f"<br><a href='{link}' target='_blank'>{song['name']} by {song['artist']} ({platform})</a>"
        return jsonify({
            "reply": f"🎶 Here are some songs for your {user_mood} mood:<br>{song_names}<br><br>Would you like to hear more songs?"})
    else:
        return jsonify({"reply": "Sorry, I couldn't find any songs for that mood. Try again!"})


if __name__ == "__main__":
    app.run(debug=True)
