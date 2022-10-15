from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from werkzeug.utils import secure_filename
import os
import time
from pydub import AudioSegment


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = ['mp3', 'm4a']

token = open('api_token.txt')
API_TOKEN = token.readline()

SENTIMENT_ENUM = {'POSITIVE': 1, 
                  'NEUTRAL': 0, 
                  'NEGATIVE': -1}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/", methods=['GET'])
def hello_world():
    return "hello, world!"


@app.route("/initial_sentiment", methods=['POST'])
def get_initial_sentiments():
    f_name = request.files['file'].filename
    upload_speech(request.files['file'])

    # TODO: generate splicing of audio for labels in order
    sentiments = get_sentiments_data(f_name)

    timestamps = {'A': [], 'B': []}

    for s in sentiments['sentiment_analysis_results']:
        if s['speaker'] in timestamps:
            timestamps[s['speaker']].append((s['start'], s['end']))
    
    # Create new audio splice files

    os.remove(os.path.join(UPLOAD_FOLDER, f_name))

    return sentiments

@app.route("/sentiment", methods=['POST'])
def get_sentiments():
    f_name = request.files['file'].filename
    upload_speech(request.files['file'])

    # TODO: splice in audio for each label in desired order (A > B > C > etc)


    return get_sentiments_data(f_name)

# Doc Page: https://www.assemblyai.com/docs/audio-intelligence#sentiment-analysis
def get_sentiments_data(f_name, delete_file=True):
    headers_0 = {'authorization': API_TOKEN}
    response_0 = requests.post('https://api.assemblyai.com/v2/upload',
                            headers=headers_0,
                            data=read_file(os.path.join(UPLOAD_FOLDER, f_name)))
    
    # deletes file after being uploaded to AssemblyAI
    if delete_file:
        os.remove(os.path.join(UPLOAD_FOLDER, f_name))

    f_link = response_0.json()['upload_url']

    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        "audio_url": f_link, # have audio url from some source
        "sentiment_analysis": True,
        "speaker_labels": True,
    }
    headers = {
        "authorization": API_TOKEN,
        "content-type": "application/json"
    }

    start_time = time.time()
    elapsed_time = 0

    response = requests.post(endpoint, json=json, headers=headers)

    new_endpoint = "https://api.assemblyai.com/v2/transcript/" + response.json()['id']

    while elapsed_time < 15:
        time.sleep(0.5)

        response = requests.get(new_endpoint, headers={'authorization': API_TOKEN})

        status = response.json()['status']

        if (status == 'completed' or status == 'error'):
            break

        elapsed_time = time.time() - start_time
        
    return jsonify(process_sentiment_json(response.json()))

def process_sentiment_json(json):
    sentiments = {}
    sentiments['sentiment_analysis_results'] = json['sentiment_analysis_results']
    avg_sent = 0

    for res in sentiments['sentiment_analysis_results']:
        avg_sent += float(res['confidence']) * SENTIMENT_ENUM[res['sentiment']]
    
    sentiments['average'] = avg_sent / len(sentiments['sentiment_analysis_results'])

    return sentiments
    
def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

def upload_speech(f):
    if f and allowed_filename(f.filename):
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

def allowed_filename(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run()