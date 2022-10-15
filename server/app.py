from flask import Flask, request
from flask_cors import CORS
import requests
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = 'mp3'
token = open('api_token.txt')
API_TOKEN = token.readline()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/", methods=['GET'])
def hello_world():
    return "hello, world!"

# Doc Page: https://www.assemblyai.com/docs/audio-intelligence#sentiment-analysis
@app.route("/sentiment", methods=['POST', 'GET'])
def get_sentiment_labels():
    f_loc = upload_speech()["upload_url"]

    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        "audio_url": f_loc, # have audio url from some source
        "sentiment_analysis": True
    }
    headers = {
        "authorization": API_TOKEN,
        "content-type": "application/json"
    }
    response = requests.post(endpoint, json=json, headers=headers)
    username = {"username": 'hi'}
    #return response.json()
    return username

def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

    headers = {'authorization': API_TOKEN}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                            headers=headers,
                            data=read_file(filename))
    
    # deletes file after being uploaded to AssemblyAI
    os.remove(os.path.join(UPLOAD_FOLDER, filename))

    return response.json()

def upload_speech():
    f = request.files['file']
    if f and allowed_filename(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

def allowed_filename(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run()