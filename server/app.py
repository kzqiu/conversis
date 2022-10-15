from flask import Flask, request
from flask_cors import CORS
import requests
from werkzeug.utils import secure_filename
import os
import time

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = ['mp3', 'm4a']
token = open('api_token.txt')
API_TOKEN = token.readline()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route("/", methods=['GET'])
def hello_world():
    return "hello, world!"

# Doc Page: https://www.assemblyai.com/docs/audio-intelligence#sentiment-analysis
@app.route("/sentiment", methods=['POST'])
def get_sentiments():
    f_name = request.files['file'].filename

    if f_name != '': 
        upload_speech(request.files['file'])

        headers_0 = {'authorization': API_TOKEN}
        response_0 = requests.post('https://api.assemblyai.com/v2/upload',
                                headers=headers_0,
                                data=read_file(os.path.join(UPLOAD_FOLDER, f_name)))
        
        # deletes file after being uploaded to AssemblyAI
        os.remove(os.path.join(UPLOAD_FOLDER, f_name))

        f_link = response_0.json()['upload_url']

        endpoint = "https://api.assemblyai.com/v2/transcript"
        json = {
            "audio_url": f_link, # have audio url from some source
            "sentiment_analysis": True
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
            
        return response.json()
    
    return {}

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