# TuneBot 🎵  


## Description
TuneBot is a chatbot web application built with Flask that helps you discover music tailored to your mood.

[//]: # (## Live Demo &#40;Deployed on Render&#41;)

[//]: # (You can access the [live version]&#40;https://tunebot-gaq4.onrender.com/&#41;)

# Installation
## Clone the repository
git clone https://github.com/f-osss/TuneBot.git

## Navigate to the project directory
```
cd TuneBot
```

## Set up the virtual environment
### For Windows:
```
tunebot_env\Scripts\activate
```

### For macOS:
```
source tunebot_env/bin/activate
```


## Install dependencies
```
pip install -r requirements.txt
```

## Environment Variables
Create a .env file with the following details:
``
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
``

You’ll need a [Spotify Developer Account](https://developer.spotify.com/dashboard) to obtain these .

## Run the Flask app locally
```
python app.py
```

## Usage
1. Open your browser and navigate to `http://localhost:5000/`.
2. Type a message regarding your mood in the TuneBot and click "Send".
3. Receive a response from the TuneBot.


