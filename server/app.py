from flask import Flask, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/", methods=['GET'])
def hello_world():
    return "hello, world!"

# Doc Page: https://www.assemblyai.com/docs/core-transcription#speaker-labels-speaker-diarization
@app.route("/labels", methods=['POST'])
def get_speech_labels():
    post_data = request.get_json()
    
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        "audio_url": "",
        "speaker_labels": True
    }
    headers = {
        "authorization": "YOUR-API-TOKEN",
        "content-type": "application/json"
    }
    response = requests.post(endpoint, json=json, headers=headers)

    return response.json()

# Doc Page: https://www.assemblyai.com/docs/audio-intelligence#sentiment-analysis
@app.route("/sentiment", methods=['POST'])
def get_sentiment():
    post_data = request.get_json()

    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        "audio_url": "", # have audio url from some source
        "sentiment_analysis": True
    }
    headers = {
        "authorization": "YOUR-API-TOKEN",
        "content-type": "application/json"
    }
    response = requests.post(endpoint, json=json, headers=headers)
    
    return response.json()

if __name__ == "__main__":
    app.run()