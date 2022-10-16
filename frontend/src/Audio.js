import './App.css';
import MicRecorder from 'mic-recorder-to-mp3';
import React, {useEffect, useState} from 'react';
import axios from 'axios';
import Sentiment from './Sentiment';
import face from './face.png';

const Mp3Recorder = new MicRecorder({ bitRate: 64 });
class Audio extends React.Component {

  constructor(props){
    super(props);
    this.state = {
      isListening: '',
      scale: 500,
      clicking: '',
      clicked: false,
      isRecording: false,
      blobURL: '',
      isBlocked: false,
      sentiment: '',
    };
  }
a
  start = () => {
    console.log('click1');
    if (this.state.isBlocked) {
      console.log('Permission Denied');
    } else if (!this.state.clicked){
      this.setState({ isListening: "Hearing you for the first time..." });
      this.setState({clicked: true});
      Mp3Recorder
            .start()
            .then(() => {
            }).catch((e) => console.error(e));
      setTimeout(() => {
        this.firstStop();
      }, 20000);
      Mp3Recorder
                  .start()
                  .then(() => {
                  }).catch((e) => console.error(e));
      const interval = setInterval(()=>{
        console.log('loop');  
        this.stop();
          Mp3Recorder
            .start()
            .then(() => {
            }).catch((e) => console.error(e));
            }, 15000);
        this.setState({clicking: interval});
      }
  };

  firstStop = () =>{
    Mp3Recorder
      .stop()
      .getMp3()
      .then(([buffer, blob]) => {
        const file = new FormData();
        file.append('file', blob, 'audio.mp3');
        const blobURL = URL.createObjectURL(blob);
        console.log(blob);
        this.setState({ blobURL, isRecording: false });
        axios({method: "post", 
        url: "http://localhost:5000/initial_sentiment", 
        data: file, 
        headers: {"Content-Type" : "multipart/form-data"},})
        .then((response) => {
          console.log(response.data.average);
          this.setState({sentiment: response.data.average});
          this.setState({ scale: this.scale + this.sentiment * 50});
        })
        .catch(function(response){console.log(response);});
        this.setState({ isListening: "Listening..."});
      })
  }

  click = () => {
    console.log('click2');
    clearInterval(this.state.clicking);
    this.setState({clicked: false});
    if(this.state.clicked){
      this.setState({ isListening: "Nice conversation!" });
      Mp3Recorder
      .stop()
      .getMp3()
      .then(([buffer, blob]) => {
        const file = new FormData();
        file.append('file', blob, 'audio.mp3');
        const blobURL = URL.createObjectURL(blob);
        console.log(blob);
        this.setState({ blobURL, isRecording: false });
        axios({method: "post", 
              url: "http://localhost:5000/sentiment", 
              data: file, 
              headers: {"Content-Type" : "multipart/form-data"},})
        .then((response) => {
          console.log(response.data.average);
          this.setState({sentiment: response.data.average});
          this.setState({ scale: this.scale + this.sentiment*50});
        })
        .catch(function(response){console.log(response);});
      })
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
        this.setState({ blobURL, isRecording: false });
        axios({method: "post", 
              url: "http://localhost:5000/sentiment", 
              data: file, 
              headers: {"Content-Type" : "multipart/form-data"},})
        .then((response) => {
          console.log(response.data.average);
          this.setState({sentiment: response.data.average});
          this.setState({ scale: this.scale + this.sentiment*50});
        })
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
        <p>{ this.state.isListening }</p>
        <Sentiment data = {this.state.sentiment}/>
          <img src = {face} width={this.state.scale} onClick={!this.state.clicked ? this.start : this.click}>
          </img>
      </div>
    );
  }

}


export default Audio;
