import './App.css';
import MicRecorder from 'mic-recorder-to-mp3';
import React from 'react';
import axios from 'axios';

const Mp3Recorder = new MicRecorder({ bitRate: 64 });
class Audio extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      isRecording: false,
      blobURL: '',
      isBlocked: false,
    };
  }

  start = () => {
    if (this.state.isBlocked) {
      console.log('Permission Denied');
    } else {
      Mp3Recorder
        .start()
        .then(() => {
          this.setState({ isRecording: true });
        }).catch((e) => console.error(e));
    }
  };

  stop = () => {
    Mp3Recorder
      .stop()
      .getMp3()
      .then(([buffer, blob]) => {
        const file = new FormData();
        file.append('file', blob, 'audio.mp3');
        const blobURL = URL.createObjectURL(blob);
        console.log(blob);
        // console.log(blobURL);
        this.setState({ blobURL, isRecording: false });
        axios({method: "post", 
              url: "http://localhost:5000/sentiment", 
              data: file, 
              headers: {"Content-Type" : "multipart/form-data"},})
        .then(function(response){console.log(response);})
        .catch(function(response){console.log(response);});
      })
    };

  componentDidMount() {
    navigator.getUserMedia({ audio: true },
      () => {
        console.log('Permission Granted');
        this.setState({ isBlocked: false });
      },
      () => {
        console.log('Permission Denied');
        this.setState({ isBlocked: true })
      },
    );
  }

  render(){
    return (
      <div className="App-header">
          <button onClick={!this.state.isRecording ? this.start : this.stop}>
            Record
          </button>
          <audio src={this.state.blobURL} controls="controls" />
      </div>
    );
  }

}


export default Audio;
